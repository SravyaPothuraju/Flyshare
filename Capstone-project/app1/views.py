from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from app1.models import *
from app1.serializer import PostModelSerializer
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.views.decorators.cache import never_cache
#
# @never_cache
# @login_required(login_url='login')
def getpostPage(request):
    try:
        if request.session.get('userId'):
            return render(request,'Post/get-post.html')
    except:
        return redirect('login')
    return redirect('login')            

# @never_cache
# @login_required(login_url='login')
def helpPage(request):
    try:
        if request.session.get('userId'):
            return render(request,'Post/help.html')
    except:
        return redirect('login')
    return redirect('login')   
    
# def postPage(request):
#     return render(request,'Post/post.html')
def submit_form(request):
    try:
        if request.session.get('userId'):
            return redirect('base')
    except:
        return redirect('login')
    return redirect('login')  
    

# post created by me 
from django.shortcuts import render
from .models import PostModel
import random

def generate_random_5_digit_number():
    return str(random.randint(10000, 99999))


# i am cahnging 
# @never_cache
# @login_required(login_url='login')
def Post(request):
    try: 
        if request.session.get('userId'):
            if request.method == 'POST':

                user = request.user
        # Retrieve data from POST request
                passenger_name = request.POST.get('PassengerName')
                date_of_journey = request.POST.get('DateOfJourney')
                gender = request.POST.get('gender')
                flight_number = request.POST.get('FlightNumber')
                pnr_number = request.POST.get('PNRNumber')
                source = request.POST.get('source')
                destination = request.POST.get('destination')
                baggage_space = request.POST.get('BaggageSpace')
                checkbox = request.POST.get('checkbox') == 'on'
                baggage_number = generate_random_5_digit_number()
        
        # Create a new instance of PostModel
                new_passenger = PostModel(
                    passenger_name=passenger_name,
                    date_of_journey=date_of_journey,
                    gender=gender,
                    flight_number=flight_number,
                    pnr_number=pnr_number,
                    source=source,
                    destination=destination,
                    baggage_space=baggage_space,
                    is_checked=checkbox,
                    user=request.user,
                    baggage_number=baggage_number,
                    )

        # Save the new instance to the database
                new_passenger.save()
    # chat_rooms = PostModel.objects.filter(user=request.user).exclude(chat_room_id__isnull=True)
    # entered_rooms = chat_rooms.filter(chat_room_id=request.user.username).exclude(chat_room_id__isnull=True)
    # user_posts = PostModel.objects.filter(passenger_name=request.user.username)

            return render(request, 'Post/post.html', {
        # 'user_posts': user_posts,
        # 'chat_rooms' : chat_rooms,
        # 'entered_rooms': entered_rooms,

            })
    except:
        return redirect('login')
    return redirect('login')




class PostModelAPIView(generics.GenericAPIView):
    serializer_class = PostModelSerializer
    queryset = PostModel.objects.all()
    def get(self, request):
        qs = PostModel.objects.all()
        date_of_journey = self.request.query_params.get('date_of_journey', None)
        source = self.request.query_params.get('source', None)
        destination = self.request.query_params.get('destination', None)
        gender = self.request.query_params.get('gender', None)
        flight_number = self.request.query_params.get('flight_number', None)
        if date_of_journey:
            qs =qs.filter(date_of_journey=date_of_journey)

        if source:
            qs =qs.filter(source=source)

        if destination:
            qs =qs.filter(destination=destination)

        if flight_number:
            qs =qs.filter(flight_number=flight_number)
            
        # queryset = PostModel.objects.filter(date_of_journey=date_of_journey)
        serializer = PostModelSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self,request):
        serializer = PostModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)





class PostModelAPIView(generics.GenericAPIView):
    serializer_class = PostModelSerializer
    queryset = PostModel.objects.all()
    def get(self, request):
        qs = PostModel.objects.all()
        serializer = PostModelSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self,request):
        serializer = PostModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class PostModelAPIViewID(generics.GenericAPIView):
    serializer_class = PostModelSerializer
    queryset = PostModel.objects.all()
    def get_object(self,id):
        try:
            data = PostModel.objects.get(id=id)
            return data
        except PostModel.DoesNotExist:
            return None
    
    def get(self,request,id):
        qs = self.get_object(id)
        serializer = PostModelSerializer(qs)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def put(self,request,id):
        qs = self.get_object(id)
        serializer = PostModelSerializer(qs,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    # def delete(self,request,id):
    #     qs = self.get_object(id)
    #     if qs is None:
    #         return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
    #     qs.delete()
    #     return Response({'message': 'Post deleted successfully'}, status=status.HTTP_204_NO_CONTENT)  
    def delete(self, request, id):
        post = get_object_or_404(PostModel, id=id, user=request.user)
        post.delete()
        return Response({'message': 'Post deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


# ///changing

from django.shortcuts import render, redirect
from app1.models import Room, Message
from django.http import HttpResponse, JsonResponse

# def home(request):
#     username = request.user.username
#     return render(request, 'home.html', {'username': username})
# @never_cache
# @login_required(login_url='login')
def home(request):
    try:
        if request.session.get('userId'):
            username = request.user.username
            room = request.GET.get('room')
            return render(request, 'home.html', {'username': username, 'room': room})
    except:
        return redirect('login')
    return redirect('login')

from django.shortcuts import render, get_object_or_404
from .models import Room, Message
# @never_cache
# @login_required(login_url='login')
def room(request, room):
    if request.session.get('userId'):
        username = request.GET.get('username')
        room_obj, created = Room.objects.get_or_create(name=room)
        messages = Message.objects.none()  # Initialize as empty queryset

        if not room_obj.is_active:
            room_obj.is_active = True
            room_obj.save()
            messages = Message.objects.filter(room=room_obj)

        return render(request, 'room.html', {
            'username': username,
            'room': room,
            'room_details': room_obj,
            'messages': messages,
        })
    return redirect('login')

    


# @never_cache
# @login_required(login_url='login')
def checkview(request):

    room = request.POST.get('room_name', '')
    username = request.POST.get('username', '')
    if Room.objects.filter(name=room).exists():
        return redirect('/app1/'+room+'/?username='+username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/app1/'+room+'/?username='+username)



from .models import PostModel
@never_cache
# @login_required(login_url='login')
# @method_decorator(csrf_exempt, name='dispatch')
def send(request):
    try:
        if request.session.get('userId'):
            if request.method == 'POST':
        
        # post_model = get_object_or_404(PostModel, id=post_model_id)

                username = request.POST.get('username', '')
                room_id = request.POST.get('room_id', '')
                message = request.POST.get('message', '')
                image = request.FILES.get('image', None)
        # baggage_number=post_model

            if not (username and room_id and (message or image)):
                return JsonResponse({'error': 'Invalid parameters'})

            if image:
            # Handle image upload
                new_message = Message.objects.create(user=username, room=room_id, image=image, value = message)

            else:
            # Handle text message
                new_message = Message.objects.create(user=username, room=room_id, value=message)

            new_message.save()
            return JsonResponse({'status': 'Message sent successfully'})

        return JsonResponse({'error': 'Invalid request method'})
    except:
        return redirect('login')
    


@never_cache
@login_required(login_url='login')
def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages":list(messages.values())})

@never_cache
@login_required(login_url='login')
def getAllMessages(request):
    # username = request.GET.get('user')
    user = request.user.username  # Get the authenticated user
    # print(user)
    # room_details = Room.objects.get(name=room)
    messages = Message.objects.filter(user=user)
   
   
    message_list = []
 
    for message in messages:
        try:
            # Try to fetch the Room with the given name
            room = get_object_or_404(Room, pk=message.room)
            room_name = get_room_name_helper(room.pk)  # Call helper function to get room_name
        except Room.DoesNotExist:
            # Handle the case where the Room does not exist
            room_name = None
 
        message_data = {
            'id': message.id,
            'value': message.value,
            'date': message.date,
            'user': message.user,
            'image': message.image.url if message.image else '',
            'room': message.room,
            'room_name': room_name,
        }
 
        message_list.append(message_data)
 
    response_data = {'messages': message_list}
    return JsonResponse(response_data)
   
   
 
    # messages = Message.objects.filter(room=room_details.id)
    # return JsonResponse({"messages":list(messages.values())})
 
def get_room_name_helper(room_id):
    # Helper function to get the room_name
    room = get_object_or_404(Room, pk=room_id)
    return room.name
 
# @login_required
# def edit_profile(request):
#     user = request.user

#     if request.method == 'POST':
#         form = UserProfileForm(request.POST, instance=user)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Profile updated successfully!')
#             return redirect('edit_profile')
#     else:
#         form = UserProfileForm(instance=user)

#     return render(request, 'Login/edit_profile_backend.html', {'form': form})

# def edit_profilePage(request):
#     user = request.user
#     if request.method == 'POST':
#         profile_picture = request.FILES.get('profile_picture') 
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         username = request.POST.get('username')
#         email = request.POST.get('email')

#         if profile_picture:
#             user.profile_picture = profile_picture
#         if first_name:
#             user.first_name = first_name
#         if last_name:
#             user.last_name = last_name
#         if username:
#             user.username = username
#         if email:
#             user.email = email
       

#         user.save()

#         return redirect(reverse('profile') + '#Edit Profile')

#     return render(request, 'Login/edit_profile.html', {'user': user})

# from django.http import JsonResponse
# from django.urls import reverse  
# def profilePage(request):
#     user = request.user
#     if request.method == 'POST':
#         profile_picture = request.FILES.get('profile_picture') 
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         username = request.POST.get('username')
#         email = request.POST.get('email')

#         if profile_picture:
#             user.profile_picture = profile_picture
#         if first_name:
#             user.first_name = first_name
#         if last_name:
#             user.last_name = last_name
#         if username:
#             user.username = username
#         if email:
#             user.email = email
#         user.save()
#         # return JsonResponse({'success': True})
#         return redirect(reverse('profile') + '#Edit Profile')
#     user_posts = request.user.postmodel_set.all()
#     return render(request, 'Login/profile.html', {'user_posts': user_posts})
#     # return render(request, 'Login/profile.html')


# remove function for profile 




from django.http import JsonResponse
from django.urls import reverse  
@never_cache
@login_required(login_url='login')
def profilePage(request):
    user = request.user
    if request.method == 'POST':
        if 'remove_picture' in request.POST:
            # Remove the profile picture
            user.profile_picture.delete(save=True)  # This deletes the profile picture file from the storage
            user.profile_picture = None  # Set the profile picture field to None in the database
            user.save()
       
        profile_picture = request.FILES.get('profile_picture') 
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')

        if profile_picture:
            user.profile_picture = profile_picture
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if username:
            user.username = username
        if email:
            user.email = email
        user.save()
       
        return redirect(reverse('profile') + '#Edit Profile')
    user_posts = request.user.postmodel_set.all()
    return render(request, 'Login/profile.html', {'user_posts': user_posts})



def change_passwordPage(request):
    return render(request, 'Login/change.html')

def verifyPage(request):
    return render(request, 'Login/verify.html')
def chat_view(request):
    return render(request, 'post/chat.html')

def termsPage(request):
    return render(request, 'Post/terms.html')

from django.shortcuts import render
from django.core.mail import send_mail
from django.http import JsonResponse



def submit_contact_formPage(request):
    if request.method == 'POST':
        # Check if user is authenticated
        if request.user.is_authenticated:
            # Get form data

            query = request.POST.get('query')

            # Compose email content
            subject = f'Contact Form Submission - {request.user.username}'
            message = f'Query: {query}\n\n\nSender Email: {request.user}'

            try:
                # Send email
                send_mail(subject, message, settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER])
                # Return JSON response indicating success
                return JsonResponse({'success': True, 'message': 'We received your help request. We will get back to you soon.'})
            except Exception as e:
                # Handle exceptions
                return JsonResponse({'success': False, 'message': f'Failed to send email: {str(e)}'})
        else:
            return JsonResponse({'success': False, 'message': 'User is not authenticated.'})
    else:
        # Handle cases where the request method is not POST
        return JsonResponse({'success': False, 'message': 'Invalid request method.'})
