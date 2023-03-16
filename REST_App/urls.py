from rest_framework.routers import DefaultRouter
from .views import StudentModelViewSet,StudentViewset, EmployeeModelViewsSet

router = DefaultRouter()
router.register(r'studs', StudentModelViewSet, basename="student")
router.register(r'stud', StudentViewset, basename= "stud")
router.register(r'emps', EmployeeModelViewsSet, basename = "employee" )

new_urlpatterns = router.urls