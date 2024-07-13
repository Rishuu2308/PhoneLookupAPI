from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Contact, UserContactMap, UserProfile
from .serializers import ContactSerializer
from django.db import IntegrityError

@permission_classes((AllowAny,))
class UserRegistrationView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")
        phone = request.data.get("phone")

        # Ensure all required fields are provided
        if not username or not password or not email or not phone:
            return Response(
                {"Error": "Username, password, phone, and email are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.create_user(username=username, password=password, email=email)
            UserProfile.objects.create(user=user, phone=phone, email_address=email)
            user.save()

            return Response({"Message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            # Handle specific errors such as duplicate phone number
            if 'UNIQUE constraint failed: api_userprofile.phone' in str(e):
                return Response(
                    {"Error": "A user with that phone number already exists"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            return Response(
                {"Error": "A user with that email already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"Error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
@permission_classes((AllowAny,))
class UserLoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        # Ensure both username and password are provided
        if not username or not password:
            return Response(
                {"Error": "Username and password are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Generate or retrieve the token for the user
            token, created = Token.objects.get_or_create(user=user)
            return Response({"Token": token.key}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"Error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

class ContactListGetView(APIView):
    def get(self, request):
        all_contacts = Contact.objects.all()
        serialized_contacts = ContactSerializer(all_contacts, many=True)
        return Response(serialized_contacts.data)

class ContactListPostView(APIView):
    def post(self, request):
        contact_name = request.data.get("name")
        contact_phone = request.data.get("phone")
        contact_email = request.data.get("email_address", None)

        if not contact_name or not contact_phone:
            return Response(
                {"Error": "Both name and phone are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        new_contact = Contact.objects.create(
            full_name=contact_name,
            phone=contact_phone,
            email_address=contact_email,
        )
        UserContactMap.objects.create(
            user=request.user,
            contact=new_contact,
        )
        return Response({"Message": "Contact added successfully!"}, status=status.HTTP_201_CREATED)


class MarkContactAsSpamView(APIView):
    def post(self, request):
        contact_phone = request.data.get("phone")
        if not contact_phone:
            return Response(
                {"Error": "Phone number required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        updated_contacts = Contact.objects.filter(phone=contact_phone).update(is_spam=True)
        updated_profiles = UserProfile.objects.filter(phone=contact_phone).update(is_spam=True)

        if updated_contacts or updated_profiles:
            return Response({"Message": "Contact marked as spam successfully!"}, status=status.HTTP_200_OK)
        return Response({"Error": "Phone number not found"}, status=status.HTTP_404_NOT_FOUND)

class SearchByNameView(APIView):
    def get(self, request):
        search_name = request.data.get("name")
        if not search_name:
            return Response(
                {"Error": "Name is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        profiles_start = UserProfile.objects.filter(user__username__startswith=search_name)
        profiles_contain = UserProfile.objects.filter(user__username__contains=search_name).exclude(user__username__startswith=search_name)
        contacts_start = Contact.objects.filter(full_name__startswith=search_name)
        contacts_contain = Contact.objects.filter(full_name__contains=search_name).exclude(full_name__startswith=search_name)

        results = [
            {
                "name": profile.user.username,
                "phone": profile.phone,
                "spam": profile.is_spam,
            }
            for profile in profiles_start | profiles_contain
        ] + [
            {
                "name": contact.full_name,
                "phone": contact.phone,
                "spam": contact.is_spam,
            }
            for contact in contacts_start | contacts_contain
        ]

        return Response(results, status=status.HTTP_200_OK)

class SearchByPhoneView(APIView):
    def get(self, request):
        search_phone = request.data.get("phone")
        if not search_phone:
            return Response(
                {"Error": "Phone number required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user_profile = UserProfile.objects.filter(phone=search_phone).first()
        if user_profile:
            user = User.objects.filter(id=user_profile.user.id, is_active=True).first()
            return Response(
                {
                    "name": user.username,
                    "phone": user_profile.phone,
                    "spam": user_profile.is_spam,
                    "email": user_profile.email_address
                }
            )

        contacts = Contact.objects.filter(phone=search_phone)
        serialized_contacts = ContactSerializer(contacts, many=True)
        return Response(serialized_contacts.data)
