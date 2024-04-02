## Sample

https://github.com/Adityak8340/SmashCast/assets/140245948/2ddbcdde-d2e0-482f-b63e-18a3ed5187bd

ample


# SmashCast - Weather-Driven Badminton Play Predictor

SmashCast is a Streamlit web application that predicts whether it's suitable to play badminton based on real-time weather data. It uses Naive Bayes model to make predictions and fetches weather information from the OpenWeatherMap API.

## Features

- Custom prediction: Users can input custom weather parameters (temperature, humidity, wind speed, and weather description) to get a prediction on whether it's suitable to play badminton.
- Real-time prediction: Users can get predictions based on their current location's weather conditions.
- Visual feedback: The application provides visual feedback (balloons) when the prediction suggests playing badminton.

## Getting Started

To run the application locally, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/SmashCast.git

2. Install the dependencies:

   '''bash
   pip install -r requirements.txt

3. Obtain an API key from [OpenWeatherMap](https://openweathermap.org/api) and replace `'YOUR_API_KEY'` in the code with your actual API key.

4. Run the Streamlit app:
   '''bash
   streamlit run app.py

## Usage

Upon launching the app, users are presented with options to get predictions: custom prediction or real-time prediction based on their current location.

- For real-time prediction, users can click the "Get Current Location" button to retrieve their location and obtain predictions based on the current weather conditions.
- After making a prediction, the app displays the weather information and the prediction result.

## Dependencies

- Python 3.x
- Streamlit
- Joblib
- NumPy
- Pandas
- Requests
- scikit-learn (or sklearn)


## Contributing

Contributions are welcome! Please fork the repository, create a new branch, make your changes, and submit a pull request.


## Acknowledgments

- Thanks to OpenWeatherMap for providing weather data through their API.
- Inspiration for this project came from the desire to combine weather information with recreational activities.
