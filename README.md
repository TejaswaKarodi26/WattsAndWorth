# Watts and Worth

## Overview

**Watts and Worth** is a sustainability-focused platform that leverages machine learning to predict energy generation, CO₂ mitigation, and carbon credit potential for multiple renewable energy sources: **solar**, **wind**, **biomass**, and **hydro**. Designed especially for industries and institutions aiming to set up green projects, this tool empowers users to quantify their environmental impact based on technical and regional input parameters.

## Features

- Predict daily energy generation for four renewable energy types using pre-trained ML models.
- Calculate associated CO₂ mitigation and potential carbon credits.
- Modular web interface with dynamic input fields based on selected energy type.
- Dedicated pages: landing page, green calculator, result display, educational fact file, and about section.
- Integrated error handling for invalid inputs and model issues.

## Technologies Used

- **Python** (backend logic and ML model integration)
- **Flask** (web framework for backend routing and rendering)
- **HTML/CSS with Tailwind CSS** (for frontend design and responsiveness)
- **Scikit-learn / Pandas / NumPy** (for data processing and machine learning)
- **Joblib** (for saving and loading pre-trained models)

## How to Run the Project

1. Clone the repository:
   ```bash
   git clone https://github.com/TejaswaKarodi26/WattsAndWorth.git
   cd WattsAndWorth

2. (Optional but recommended) Create a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate   # On Windows
   source venv/bin/activate  # On macOS/Linux

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt

4. Run the application:

   ```bash
   python app.py




