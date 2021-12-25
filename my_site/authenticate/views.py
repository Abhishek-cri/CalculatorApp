from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash 
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib import messages 
import re
from django.http import HttpResponse, request
from .forms import SignUpForm, EditProfileForm 
from .models import Student
# Create your views here.
def home(request): 
	return render(request, 'authenticate/home.html', {})

def login_user (request):
	if request.method == 'POST': #if someone fills out form , Post it 
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:# if user exist
			login(request, user)
			messages.success(request,('Youre logged in'))
			return redirect('home') #routes to 'home' on successful login  
		else:
			messages.success(request,('User Not Registered'))
			return redirect('login') #re routes to login page upon unsucessful login
	else:
		return render(request, 'authenticate/login.html', {})

def logout_user(request):
	logout(request)
	messages.success(request,('Youre now logged out'))
	return redirect('home')

def register_user(request):
	if request.method =='POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request,user)
			messages.success(request, ('Youre now registered'))
			return redirect('home')
	else: 
		form = SignUpForm() 

	context = {'form': form}
	return render(request, 'authenticate/register.html', context)

def edit_profile(request):
	if request.method =='POST':
		form = EditProfileForm(request.POST, instance= request.user)
		if form.is_valid():
			form.save()
			messages.success(request, ('You have edited your profile'))
			return redirect('home')
	else: 		#passes in user information 
		form = EditProfileForm(instance= request.user) 

	context = {'form': form}
	return render(request, 'authenticate/edit_profile.html', context)
	#return render(request, 'authenticate/edit_profile.html',{})



def change_password(request):
	if request.method =='POST':
		form = PasswordChangeForm(data=request.POST, user= request.user)
		if form.is_valid():
			form.save()
			update_session_auth_hash(request, form.user)
			messages.success(request, ('You have edited your password'))
			return redirect('home')
	else: 		#passes in user information 
		form = PasswordChangeForm(user= request.user) 

	context = {'form': form}
	return render(request, 'authenticate/change_password.html', context)

def mainpage(request):
	res=render (request,'authenticate/mainpage.html')
	return res	

def calculation(request):
				if request.method=="POST":
					values=request.POST['values'] #string having whole ques
							#q=request.GET['value']
							
					try:
					
							print(values)
							vals=re.findall(r"(\d+)",values) #extrect values
							operators=['+','x','÷','-','.','%']
							opr=[]
							for v in values:
								for o in operators:
									if v==o:
										opr.append(o)
							print(opr)                      #extrect operators
							print(re.findall(r"(\d+)",values))

							for o in opr:
								if o=='.':
									i=opr.index(o)
									res=vals[i]+"."+vals[i+1]
									vals.remove(vals[i+1])
									opr.remove(opr[i])
									vals[i]=res
									print(vals)
									print(opr)
							for o in opr:
								if o=='%':
									i=opr.index(o)
									res=(float(vals[i])/100)*float(vals[i+1])
									vals.remove(vals[i+1])
									opr.remove(opr[i])
									vals[i]=res
									print(vals)
									print(opr)
							for o in opr:
								if o=='÷':
									i=opr.index(o)
									res=float(vals[i])/float(vals[i+1])
									vals.remove(vals[i+1])
									opr.remove(opr[i])
									vals[i]=str(res)
									print(vals)
									print(opr)
							for o in opr:
								if o=='x':
									i=opr.index(o)
									res=float(vals[i])*float(vals[i+1])
									vals.remove(vals[i+1])
									opr.remove(opr[i])
									vals[i]=str(res)
									print(vals)
									print(opr)
							for o in opr:
								if o=='+':
									i=opr.index(o)
									res=float(vals[i])+float(vals[i+1])
									vals.remove(vals[i+1])
									opr.remove(opr[i])
									vals[i]=str(res)
									print(vals)
									print(opr)
								if o=='-':
									i=opr.index(o)
									res=float(vals[i])-float(vals[i+1])
									vals.remove(vals[i+1])
									opr.remove(opr[i])
									vals[i]=str(res)
									print(vals)
									print(opr)


							if len(opr)!=0:
								if opr[0]=='÷':
									result = float(vals[0])/float(vals[1])
								elif opr[0]=='x':
									result = float(vals[0])*float(vals[1])
								elif opr[0]=='+':
									result = float(vals[0])+float(vals[1])
								else :
									result = float(vals[0])-float(vals[1])
							else:
								result = float(vals[0])

							final_result=round(result,2)
							print(final_result)

							res=render(request,'authenticate/mainpage.html',{'result':final_result,'values':values})

							return res

							ans=eval(values)
							showerror={
								"q":values,
								"ans":ans,
								"error":False
							}
							
					except:
						
						return render (request,'authenticate/mainpage.html',context={"error":True})
	


	

			
				

				
		




			







	# showerror = {
	# 					"values":values,
	# 					"result":final_result,
	# 					"error": False
	# 				}
	# 				return res
	# 			except:	
	# 				showerror={
	# 					"error":True
	# 				}

			# def calculation(request):
			# if request.method=="POST":
			#     values=request.POST['values'] 

			# result=float(stack.pop())
			# final_result=round(result,2)
			# res=render(request,'authenticate/mainpage.html',{'result':final_result,'values':values})
			#return res