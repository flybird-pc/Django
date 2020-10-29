from django.test import TestCase

# Create your tests here.

from django.test import TestCase  # django.test.TestCase从unittest.TestCase继承而来
from sign.models import Event, Guest


# Create your tests here.
class ModelTest(TestCase):
    def setUp(self):
        # 创建数据，但此数据不会真的向数据库表中插入数据
        Event.objects.create(id=4, name="django测试", status=True, limit=10, address="ziyang",
                             start_time="2018-07-19 02:38:28")
        Guest.objects.create(id=6, event_id=4, real_name="李大龙", phone="13678946352", email="lidalong@qq.com", sign=False)

    def test_event_models(self):
        result = Event.objects.get(name="django测试")
        self.assertEqual(result.address, "ziyang")
        self.assertTrue(result.status)

    def test_guest_models(self):
        result = Guest.objects.get(real_name="李大龙")
        self.assertEqual(result.phone, "13678946352")
        self.assertFalse(result.sign)
