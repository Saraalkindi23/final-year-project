from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
import joblib
# Load models once when the server starts
fbinary_model = joblib.load('fbinary_model.pkl')
ftype_model = joblib.load('ftype_model.pkl')

from django.shortcuts import render
import pandas as pd
import joblib

# Load the trained models
gbinary_model = joblib.load('binary_model_garage.pkl')
gtype_model = joblib.load('type_model_garage.pkl')


# Load the trained models
gpsbinary_model = joblib.load('binary_model_gps.pkl')
gpstype_model = joblib.load('type_model_gps.pkl')


# Load models
lightbinary_model = joblib.load('binary_model_light.pkl')
lighttype_model = joblib.load('type_model_light.pkl')

def light_prediction(request):
    attack_detection = None
    attack_type = None

    if request.method == 'POST':
        # Get the user inputs from the form
        motion_status = int(request.POST['motion_status'])
        light_status = int(request.POST['light_status'])
        hour = int(request.POST['hour'])
        day_of_week = int(request.POST['day_of_week'])

        # Prepare the data for prediction
        new_data = pd.DataFrame({
            'motion_status': [motion_status],
            'light_status': [light_status],
            'hour': [hour],
            'day_of_week': [day_of_week]
        })

        # Make predictions
        attack_detection = lightbinary_model.predict(new_data)[0]
        if attack_detection == 1:
            attack_type = lighttype_model.predict(new_data)[0]
        else:
            attack_type = "No attack detected"

    return render(request, 'home/light.html', {
        'attack_detection': attack_detection,
        'attack_type': attack_type,
    })




def gps_predict(request):
    attack = None
    attack_type = None

    if request.method == 'POST':
        # Get input from the form
        latitude = float(request.POST.get('latitude'))
        longitude = float(request.POST.get('longitude'))

        # Create DataFrame from input
        new_data = {
            'latitude': [latitude],
            'longitude': [longitude]
        }
        new_df = pd.DataFrame(new_data)

        # Predict whether there is an attack or not (binary classification)
        attack_prediction = gpsbinary_model.predict(new_df)

        if attack_prediction[0] == 1:
            attack = "Attack detected!"
            # Predict the type of attack (if an attack is detected)
            attack_type_prediction = gpstype_model.predict(new_df)
            attack_type = attack_type_prediction[0]
        else:
            attack = "No attack detected."

    return render(request, 'home/gps.html', {'attack': attack, 'attack_type': attack_type})


# Function to predict attack status and type
def predict_attack(door_state, sphone_signal, hour, minute, day_of_week):
    # Create a DataFrame with the input features
    input_data = pd.DataFrame({
        'door_state': [door_state],
        'sphone_signal': [sphone_signal],
        'hour': [hour],
        'minute': [minute],
        'day_of_week': [day_of_week]
    })

    # Predict if an attack is happening (binary classification)
    attack_prediction = gbinary_model.predict(input_data)[0]

    # If the model predicts an attack, classify the attack type
    if attack_prediction == 1:
        attack_type_prediction = gtype_model.predict(input_data)[0]
        return attack_prediction, attack_type_prediction
    else:
        return attack_prediction, None  # No attack detected

# View function for the garage prediction page
def garage_predict(request):
    attack = None
    attack_type = None

    if request.method == 'POST':
        # Get input data from the form
        door_state = int(request.POST['door_state'])
        sphone_signal = int(request.POST['sphone_signal'])
        hour = int(request.POST['hour'])
        minute = int(request.POST['minute'])
        day_of_week = int(request.POST['day_of_week'])

        # Predict attack status and type
        attack, attack_type = predict_attack(door_state, sphone_signal, hour, minute, day_of_week)

    return render(request, 'home/garage.html', {'attack': attack, 'attack_type': attack_type})




def fridge_prediction(request):
    if request.method == 'POST':
        try:
            # Get input values from the user
            fridge_temp = float(request.POST['fridge_temp'])
            temp_condition = request.POST['temp_condition']
            temp_condition_encoded = 1 if temp_condition.lower() == 'high' else 0

            # Prepare the input data
            input_data = [[fridge_temp, temp_condition_encoded]]

            # Predict whether it's an attack or normal
            is_attack = fbinary_model.predict(input_data)[0]
            attack_type = None
            if is_attack == 1:
                attack_type = ftype_model.predict(input_data)[0]

            # Return prediction results
            context = {
                'is_attack': is_attack,
                'attack_type': attack_type if is_attack == 1 else None,
            }
            return render(request, 'home/fridge.html', context)

        except Exception as e:
            return render(request, 'home/fridge.html', {'error': str(e)})

    return render(request, 'home/fridge.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('iot')  # Redirect to home page after successful login
        else:
            # Authentication failed, re-render login with error message
            return render(request, 'home/login.html', {'error': 'Invalid username or password'})

    return render(request, 'home/login.html')


def home(request):
    return render(request, 'home/home.html')  # Renders the home.html template


def fridge(request):
    return render(request, 'home/fridge.html')

def garage(request):
    return render(request, 'home/garage.html')

def light(request):
    return render(request, 'home/light.html')
def iot(request):
    return render(request, 'home/iot.html')
def gps(request):
    return render(request, 'home/gps.html')
