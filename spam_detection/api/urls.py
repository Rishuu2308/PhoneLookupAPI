from django.urls import path
from .views import ContactListGetView,ContactListPostView,UserRegistrationView, UserLoginView, MarkContactAsSpamView, SearchByNameView, SearchByPhoneView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user_register'),
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('get_contacts/', ContactListGetView.as_view(), name='contacts_list'),
    path('post_contacts/', ContactListPostView.as_view(), name='contacts_list'),
    path('mark_spam/', MarkContactAsSpamView.as_view(), name='mark_as_spam'),
    path('search_name/', SearchByNameView.as_view(), name='search_by_name'),
    path('search_phone/', SearchByPhoneView.as_view(), name='search_by_phone'),
]
