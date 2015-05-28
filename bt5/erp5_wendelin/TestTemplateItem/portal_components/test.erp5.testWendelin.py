##############################################################################
#
# Copyright (c) 2002-2015 Nexedi SA and Contributors. All Rights Reserved.
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsibility of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# guarantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
##############################################################################

from Products.ERP5Type.tests.ERP5TypeTestCase import ERP5TypeTestCase
import msgpack
import numpy as np
import transaction

class Test(ERP5TypeTestCase):
  """
  Wendelin Test
  """

  def getTitle(self):
    return "Wendelin Test"

  def afterSetUp(self):
    """
    This is ran before anything, used to set the environment
    """
    # here, you can create the categories and objects your test will depend on
    pass

  def test_0_import(self): 		 
    """ 		 
    Test we can import certain libraries but still failure to do so should be a  		 
    a test step failure rather than global test failure. 		 
    """ 		 
    import scipy 		 
    import sklearn
  def test_01_IngestionFfromFluentd(self):
    """
    Test ingestion using a POST Request containing a msgpack encoded message
    simulating input from fluentd
    """
    portal = self.portal
    request = portal.REQUEST
    
    # simulate fluentd by setting proper values in REQUEST
    request.method = 'POST'
    real_data_dictionary = {'1':'1'}
    data_chunk = msgpack.packb([0, real_data_dictionary], use_bin_type=True)
    request.set('reference', 'car')
    request.set('data_chunk', data_chunk)
    
    # do real ingestion call
    portal.portal_ingestion_policies.wendelin_car_logs.ingest()
    data_stream = portal.data_stream_module.wendelin_22
    
    # ingestion handler script saves new data using new line so we 
    # need to remove it, it also stringifies thus we need to
    data_stream_data = data_stream.getData()
    data_stream_data = data_stream_data.replace('\n', '')
    self.assertEqual(str(real_data_dictionary), data_stream_data)
    
    # XXX: try sample transformation
    
  def test_02_Transformations(self):
    """
      Test we can use python scientific libraries by using directly created
      Wendelin examples.
    """
    portal = self.portal
    portal.game_of_life()
    # XXX: for now following ones are disabled as wendelin.core not available
    # in testnodes framework
    # portal.game_of_life_out_of_core()
    # portal.game_of_life_out_of_core_activities()
    
  def test_03_DataArray(self):
    """
      Test persistently saving a ZBig Array to a Data Array.
    """
    from wendelin.bigarray.array_zodb import ZBigArray
    
    data_array = self.portal.data_array_module.newContent( \
                   portal_type = 'Data Array')
    array = ZBigArray((60,60), np.uint8)
    
    # ZBigArray requirement: before we can compute it (with subobject
    # .zfile) have to be made explicitly known to connection or current
    # transaction committed
    transaction.commit()
  
    data_array.setArray(array)
    self.tic()
    
    # test array stored and we teturn ZBig Array instance
    persistent_zbig_array = data_array.getArray()
    self.assertEqual(ZBigArray, persistent_zbig_array.__class__)
    self.assertEquals(array, persistent_zbig_array)
    
    # try to resize it
    #pure_numpy_array = persistent_zbig_array[:,:] # ZBigArray -> ndarray view of it
    #pure_numpy_array = np.resize(pure_numpy_array, (100,100))
    #self.assertNotEquals(pure_numpy_array.shape, persistent_zbig_array.shape)
    
    # resize Zbig Array
    #persistent_zbig_array.resize(100,100)