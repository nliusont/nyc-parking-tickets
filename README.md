# NYC Alternate Side Parking Violations App

This Streamlit app visualizes data on alternate side parking violations in New York City. The app uses interactive maps and charts to display where and when most violations occur, helping users understand patterns and trends.

## Features

- **Interactive Map**: A scatter plot heatmap of NYC violations, showing density of violations by location.
- **Monthly Violations Chart**: A line chart displaying violations by month.
- **Hourly Violations Chart**: A line chart displaying violations by hour of the day.
- **Data Source**: Based on NYC Open Data's [parking violations dataset](https://data.cityofnewyork.us/City-Government/Open-Parking-and-Camera-Violations/nc67-uf89/about_data) for FY24.

## Libraries Used

- **Streamlit**: Used for building the interactive web app.
- **Pandas**: For data manipulation and processing.
- **NumPy**: For numerical operations and calculations.
- **Plotly**: To create interactive scatter plot heatmaps.
- **Altair**: For creating simple and intuitive line charts.

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/your-username/nyc-parking-violations.git
   cd nyc-parking-violations```

2. ```pip install -r requirements.txt```

3. ```streamlit run app.py```