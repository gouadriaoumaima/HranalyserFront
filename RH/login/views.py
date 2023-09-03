from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# importing render and redirect
from django.shortcuts import render, redirect
# importing the openai API
import openai
# import the generated API key from the secret_key file

# loading the API key from the secret_key file
openai.api_key = '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'
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')



def user_logout(request):
    logout(request)
    return redirect('login')

def chat(request):
    return render(request, 'chat.html')

def new_chat(request):
    # clear the messages list
    request.session.pop('messages', None)
    return redirect('home')
import PyPDF2



import docx2txt

def extract_text_from_docx(file):
    text = docx2txt.process(file)
    return text

def extract_text_from_pdf(file):
    text = ""
    pdf_reader = PyPDF2.PdfReader(file)
    num_pages = len(pdf_reader.pages)
    for page_num in range(num_pages):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()

    return text

@login_required
def home(request):
    try:
        # if the session does not have a messages key, create one
        if 'messages' not in request.session:
            request.session['messages'] = [
                {"role": "system", "content": "You are now chatting with a user, provide them with comprehensive, short and concise answers."},
            ]

        if request.method == 'POST':
            # get the prompt from the form
            prompt = request.POST.get('prompt')
            # get the temperature from the form
            file = request.FILES.get('file')  # Récupérez le fichier du formulaire
            if file:
              file_extension = file.name.split('.')[-1]
              if file_extension.lower() == 'pdf':
                extracted_text = extract_text_from_pdf(file)
                prompt += "\n" + extracted_text
              elif file_extension.lower() == 'docx':
                extracted_text = extract_text_from_docx(file) 
                prompt += "\n" + extracted_text 
              else:
                
            
                # Lisez le contenu du fichier (exemple avec un fichier texte)
                  file_content = file.read().decode('utf-8')
                # Ajoutez le contenu du fichier au prompt
                  prompt += "\n" + file_content
            # append the prompt to the messages list
            request.session['messages'].append({"role": "user", "content": prompt})
            # set the session as modified
            request.session.modified = True
            # call the openai API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=request.session['messages'],
              
                max_tokens=1000,
            )
            # format the response
            formatted_response = response['choices'][0]['message']['content']
            # append the response to the messages list
            request.session['messages'].append({"role": "assistant", "content": formatted_response})
            request.session.modified = True
            # redirect to the home page
            context = {
                'messages': request.session['messages'],
                'prompt': '',
               
            }
            return render(request, 'home.html', context)
        else:
            # if the request is not a POST request, render the home page
            context = {
                'messages': request.session['messages'],
                'prompt': '',
             
            }
            return render(request, 'home.html', context)
    except Exception as e:
        print(e)
        # if there is an error, redirect to the error handler
    return render(request, 'home.html')

def Register(request):
    if request.method=='POST':
        context = {'has_error': False, 'data': request.POST}
        username=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password')
        pass2=request.POST.get('password2')
        if len(pass1) < 6:
            messages.add_message(request, messages.ERROR,'Password should be at least 6 characters')
            context['has_error'] = True

        if pass1 != pass2:
            messages.add_message(request, messages.ERROR,'Password mismatch')
            context['has_error'] = True
            
        if not username:
            messages.add_message(request, messages.ERROR,'Username is required')
            context['has_error'] = True

        if User.objects.filter(username=username).exists():
            messages.add_message(request, messages.ERROR,'Username is taken, choose another one')
            context['has_error'] = True
            return render(request, 'signup.html', context, status=409)
        if User.objects.filter(email=email).exists():
            messages.add_message(request, messages.ERROR,
                                 'Email is taken, choose another one')
            context['has_error'] = True

            return render(request, 'signup.html', context, status=409)
        if context['has_error']:
            return render(request, 'signup.html', context)
        my_user = User.objects.create_user(username=username,email=email,password=pass1)
        my_user.set_password(pass1)
        my_user.save()

        if not context['has_error']:
            return redirect('login')
         
    return render(request, 'register.html')