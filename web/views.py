from django.shortcuts import render,redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm
import pandas as pd
import joblib

def index(request):
    return render(request,'index.html')



from .forms import CustomUserCreationForm

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')

def profile(request):
    return render(request,'profile.html')

def prediction(request):
    return render(request,'pedict.html')

try:
    diabetes_model = joblib.load('web/diabetes_model.pkl')
    cvd_model = joblib.load('web/cvd_model.pkl')
    print("✅ Models loaded successfully!")
except Exception as e:
    print(f"❌ Error loading models: {str(e)}")
    diabetes_model = None
    cvd_model = None


def cvdform(request):
    return render(request,'cvd_form.html')



def cvd(request):
    
    if not cvd_model:
        return render(request,'result.html', {'prediction':"Error: CVD model not loaded"}, {'model_type':"CVD"})
    
    try:
        if request.method=='POST':
            
            patient_data = {
                    'age': float(request.POST.get('age')),
                    'gender': request.POST.get('gender',0),
                    'ap_hi': float(request.POST.get('systolic-bp')),
                    'ap_lo': float(request.POST.get('diastolic-bp')),
                    'cholesterol': float(request.POST.get('cholesterol')),
                    'smoke': request.POST.get('smoking-status'),
                    'weight': float(request.POST.get('weight'))
                    }
            

            input_df = pd.DataFrame([patient_data])[cvd_model['features']['cvd']]
            scaled_data = cvd_model['scaler_cvd'].transform(input_df)
            risk_prob = cvd_model['cvd_model'].predict_proba(scaled_data)[0][1]

        
            risk_level = "🚨 High Risk" if risk_prob > 0.7 else "✅ Low Risk"
            result = f"""
            <h3>CVD Risk: <strong>{risk_prob:.1%}</strong></h3>
            <p class="risk-level { 'high-risk' if risk_prob > 0.7 else 'low-risk' }">{risk_level}</p>
            <h4>Recommendations:</h4>
            <ul>
                <li>{"Consult a cardiologist immediately" if risk_prob > 0.7 else "Maintain healthy lifestyle"}</li>
                <li>{"Get an ECG test" if risk_prob > 0.7 else "Regular BP monitoring"}</li>
            </ul>
            """
        return render(request,'result.html', {'prediction':result,'model_type':'CVD'})

    except Exception as e:
        err=f"Error: {str(e)}"
        return render(request,'result.html', {'prediction':err, 'model_type':"CVD"})
    
def diabaticform(request):
    return render(request,'diabetic_form.html')    
    
def diabatic(request):
    if diabetes_model is None:
        return render(request,'error.html',message="Diabetes model not loaded. Please try again later.")
    
    try:
        if request.method=='POST':
            patient_data = {
                'Pregnancies': float(request.POST.get('pregnancies')),
                'Glucose': float(request.POST.get('glucose')),
                'BloodPressure': float(request.POST.get('blood-pressure')),
                'SkinThickness': float(request.POST.get('skin-thickness')),
                'Insulin': float(request.POST.get('insulin')),
                'BMI': float(request.POST.get('bmi')),
                'DiabetesPedigreeFunction': float(request.POST.get('diabetes-pedigree')),
                'Age': float(request.POST.get('age'))
            }
            print(patient_data)

            features = pd.DataFrame([patient_data])[diabetes_model['features']['diabetes']]
            scaled_features = diabetes_model['scaler_diabetes'].transform(features)
            
            
            probability = diabetes_model['diabetes_model'].predict_proba(scaled_features)[0][1]
            prediction = "Diabetic" if probability > 0.5 else "Not Diabetic"
            
            
            if probability > 0.7:
                risk_level = "High"
                recommendations = [
                    "Immediate HbA1c test recommended",
                    "Consult an endocrinologist",
                    "Start lifestyle intervention",
                    "Monitor glucose levels daily"
                ]
            elif probability > 0.4:
                risk_level = "Moderate"
                recommendations = [
                    "Schedule glucose tolerance test",
                    "Improve diet and exercise",
                    "Monitor symptoms"
                ]
            else:
                risk_level = "Low"
                recommendations = [
                    "Maintain healthy lifestyle",
                    "Annual checkup recommended"
                ]

            
            result = {
                'probability': f"{probability:.1%}",
                'prediction': prediction,
                'risk_level': risk_level,
                'key_indicators': {
                    'Glucose': patient_data['Glucose'],
                    'BMI': patient_data['BMI'],
                    'Age': patient_data['Age']
                },
                'recommendations': recommendations,
                'all_data': patient_data
            }
            print(result)
            return render(request,'dibatic_result.html',result)

    except KeyError as e:
        err=f"Missing required field: {str(e)}"
        return render(request,'result.html',{'prediction':err,'model_type':'Diabatic'})
    except ValueError as e:
        err=f"value error: {str(e)}"
        return render(request,'result.html',{'prediction':err,'model_type':'Diabatic'})
    except Exception as e:
        err=f"Prediction error: {str(e)}"
        return render(request,'result.html',{'prediction':err,'model_type':'Diabatic'})

    

