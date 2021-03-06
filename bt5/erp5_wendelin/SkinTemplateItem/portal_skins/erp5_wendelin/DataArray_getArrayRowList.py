from Products.ERP5Type.Document import newTempBase

if context.getArray() is None:
  return []
  
length = context.getArrayShape()[0]
if length == 0:
  return []

class SequenceSliceMap():
  def __init__(self, sequence_slice, usual_slice_length, total_length):
    self.sequence_slice = sequence_slice
    self.length = usual_slice_length
    self.total_length = total_length

  def __repr__(self):
    return repr(list(self))

  def __len__(self):
    return self.total_length

  def __getitem__(self, index):
    return self.sequence_slice[index % self.length]

def createTempBase(nr, row):
  def getElementFromArray(array, index):
    return array[index]

  def getElementFromScalar(scalar, index=None):
    return scalar

  column_list = [col for col in context.DataArray_getArrayColumnList() if col[0] != 'index']
  column_iterator = enumerate(column_list)
  if len(column_list) == 1:
    getElement = getElementFromScalar
  else:
    getElement = getElementFromArray
  return newTempBase(context.getPortalObject(),
                     str(id(row)),
                     index = nr,
                     **{col[0]: str(getElement(row, i)) for i, col in column_iterator})




# never access more than 1000 lines at once
list_lines = min(list_lines, limit, 1000)
list_end = list_start + list_lines

if list_end > length:
  list_end = length
  list_start = list_end - (list_end % list_lines)

if list_start == list_end:
  array_slice = [context.getArrayIndex(list_start)]
else:
  array_slice = context.getArraySlice(list_start, list_end)

temp_base_list = [createTempBase(nr + list_start, row) for nr, row in enumerate(array_slice)]

# return lazy sequence of temp objects
return SequenceSliceMap(temp_base_list, list_lines, length)
