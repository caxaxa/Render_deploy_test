
# Industry Analysis Dashboard

This project hosts a web application to visualize and analyze industry data related to advertising metrics such as Cost Per Click, Cost Per Lead, Click Through Rate, Conversion Rate, and Average ROAS. It includes comparison between Google Ads and Meta Ads across different industries.

## Directory Structure

```
app/
│
├── app.py           # Main application file
├── utils.py         # Utility functions and classes
├── templates/
│   ├── dashboard.html # HTML template for dashboard
├── data/
│   ├── updated_data.csv # CSV data file
│   ├── content.txt      # Content description text file
├── requirements.txt # Dependencies file
```

## Installation

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

To launch the dashboard, simply run:

```bash
python app.py
```

The dashboard will be accessible at `http://localhost:5006/`.

## Dashboard Overview

The dashboard consists of several components:

- **Select Ads Platform**: Dropdown to select between Google Ads and Meta Ads.
- **Select Industry**: Dropdown to choose the industry.
- **Select Metric**: Dropdown to choose the advertising metric.
- **Distribution Plot**: Visualization of the selected metric for the selected industry and platform.
- **National Averages**: Tables displaying the national averages for Meta Ads and Google Ads.

## Contribution

Feel free to contribute to this project by submitting issues, feature requests, or pull requests.
