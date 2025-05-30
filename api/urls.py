from django.urls import path,include
from rest_framework.routers import DefaultRouter
from bloodrequest.views import BloodRequestViewSet,DonationAcceptanceViewSet



router = DefaultRouter()
router.register('blood-requests', BloodRequestViewSet, basename='blood-request')
router.register('donation-acceptances', DonationAcceptanceViewSet, basename='donation-acceptance')


urlpatterns = [
    path('',include(router.urls)), 
]