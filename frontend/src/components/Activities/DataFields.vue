<template>
  <div
    class="my-3 flex items-center justify-between text-lg font-medium sm:mb-4 sm:mt-8"
  >
    <div class="flex h-8 items-center text-xl font-semibold text-ink-gray-8">
      {{ __('Data') }}
      <Badge
        v-if="document.isDirty"
        class="ml-3"
        :label="'Not Saved'"
        theme="orange"
      />
    </div>
    <div class="flex gap-1">
      <Button
        v-if="isManager() && !isMobileView"
        @click="showDataFieldsModal = true"
      >
        <EditIcon class="h-4 w-4" />
      </Button>
      <Button
        label="Save"
        :disabled="!document.isDirty"
        variant="solid"
        :loading="document.save.loading"
        @click="saveChanges"
      />
      <Button
        v-if="doctype === 'CRM Deal' && !hasRequestedSpecialPrice"
        label="Special Price"
        variant="solid"
        @click="showRequestDialog = true"
      />
    </div>
  </div>

  <div
    v-if="document.get.loading"
    class="flex flex-1 flex-col items-center justify-center gap-3 text-xl font-medium text-gray-500"
  >
    <LoadingIndicator class="h-6 w-6" />
    <span>{{ __('Loading...') }}</span>
  </div>

  <div v-else class="pb-8 relative">
    <nav class="flex border-b mb-4 space-x-4">
      <button
        v-for="tab in filteredTabs"
        :key="tab.label"
        @click="activeTabLabel = tab.label"
        :class="[
          'pb-2',
          activeTabLabel === tab.label
            ? 'border-b-2 border-blue-600 font-semibold'
            : 'text-gray-600 hover:text-gray-900',
        ]"
      >
        {{ tab.label }}
      </button>
    </nav>
    <FieldLayout
      v-if="tabs.data && document.doc"
      :tabs="filteredTabs.filter(tab => tab.label === activeTabLabel)"
      :data="document.doc"
      :doctype="doctype"
    />
    <div
      v-if="doctype === 'CRM Deal' && activeTabLabel === 'Special Price Request' && isManager()"
      class="sticky bottom-0 left-0 right-0 bg-white border-t px-4 py-3 flex justify-end gap-2"
    >
      <Button
        label="Approve"
        variant="solid"
        @click="approveSpecialPrice"
      />
    </div>
  </div>

  <DataFieldsModal
    v-if="showDataFieldsModal"
    v-model="showDataFieldsModal"
    :doctype="doctype"
    @reload="
      () => {
        tabs.reload()
        document.reload()
      }
    "
  />

  <Dialog 
    v-if="doctype === 'CRM Deal'"
    v-model="showRequestDialog"
    :options="{ size: '2xl' }"
    class="special-price-dialog"
  >
    <template #body>
      <div class="sticky top-0 z-10 bg-white border-b px-4 pt-4 pb-2">
        <div class="text-lg font-semibold text-gray-800">
          {{ __('Special Price Request Form') }}
        </div>
      </div>

      <div class="max-h-[70vh] overflow-y-auto px-4 pb-4">
        <FieldLayout
          v-if="tabs.data && document.doc"
          :tabs="tabs.data.filter(tab => tab.label === 'Special Price Request')"
          :data="document.doc"
          :doctype="doctype"
        />
      </div>
     
      <div class="sticky bottom-0 left-0 right-0 z-10 bg-white border-t px-4 py-3 flex justify-end gap-2">
        <Button variant="ghost" label="Cancel" @click="showRequestDialog = false" />
        <Button variant="solid" label="Request" @click="submitSpecialPrice" />
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import EditIcon from '@/components/Icons/EditIcon.vue'
import DataFieldsModal from '@/components/Modals/DataFieldsModal.vue'
import FieldLayout from '@/components/FieldLayout/FieldLayout.vue'
import { Badge, createResource } from 'frappe-ui'
import LoadingIndicator from '@/components/Icons/LoadingIndicator.vue'
import { usersStore } from '@/stores/users'
import { useDocument } from '@/data/document'
import { isMobileView } from '@/composables/settings'
import { ref, watch, computed } from 'vue'

const props = defineProps({
  doctype: { type: String, required: true },
  docname: { type: String, required: true },
})

const { isManager } = usersStore()

const showDataFieldsModal = ref(false)
const showRequestDialog = ref(false)
const hasRequestedSpecialPrice = ref(false)


const activeTabLabel = ref('')


const { document } = useDocument(props.doctype, props.docname)

const tabs = createResource({
  url: 'crm.fcrm.doctype.crm_fields_layout.crm_fields_layout.get_fields_layout',
  cache: ['DataFields', props.doctype],
  params: { doctype: props.doctype, type: 'Data Fields' },
  auto: true,
})

watch(
  () => document.doc,
  (doc) => {
    if (props.doctype === 'CRM Deal' && doc) {
      hasRequestedSpecialPrice.value = !!doc.has_requested_special_price
    }
  },
  { immediate: true }
)

const filteredTabs = computed(() => {
  if (!tabs.data) return []
  if (props.doctype !== 'CRM Deal') return tabs.data

  if (hasRequestedSpecialPrice.value) return tabs.data
  if (document.doc && document.doc.status === 'Request For Special Price') return tabs.data

  return tabs.data.filter(tab => tab.label !== 'Special Price Request')
  
})


watch(
  filteredTabs,
  (newTabs) => {
    if (!newTabs.find(tab => tab.label === activeTabLabel.value)) {
      activeTabLabel.value = newTabs.length ? newTabs[0].label : ''
    }
  },
  { immediate: true }
)



function saveChanges() {
  document.save.submit()
}


async function submitSpecialPrice() {
  if (props.doctype === 'CRM Deal') {
    Object.assign(document.doc, {
      status: 'Request For Special Price',
      has_requested_special_price: 1,
    })
  }

  await document.save.submit()

  hasRequestedSpecialPrice.value = true
  showRequestDialog.value = false

  tabs.reload()
}


async function approveSpecialPrice() {
  alert('Approved this special price request');

  const specialDiscount = document.doc.special_discount;

  if (document.doc.products && Array.isArray(document.doc.products)) {
    for (const product of document.doc.products) {
      product.discount_percentage = specialDiscount;
    }
    await document.save.submit();
  }
await document.reload();
tabs.reload();
}

</script>

<style scoped>

nav button {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem 1rem;
}

nav button.active {
  border-bottom: 2px solid #2563eb; 
  color: #2563eb;
}
</style>