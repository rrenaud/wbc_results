from wbc_results import *

def t(left, right):
  assert left == right, 'Failure: %s != %s' % (str(left), str(right))

t(list(GroupMatching([1,2,3,4,4,5])), [[1], [2], [3], [4,4], [5]])
t(Rankify([1,2,3,4,4,5]), [1.0,2.0,3.0,4.5,4.5,6])
