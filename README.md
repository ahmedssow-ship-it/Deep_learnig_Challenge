# Deep Learning Challenge (Regression Problem: Bike SHARING DEMAND)

## Project Team

| Field | Information |
|------|-------------|
| Institution | African Institute for Mathematical Sciences |
| Members | Ahmed Souleymane Sow, Soukeye Touré |
| Supervisor | Dr. Bousso and Tutor Diamweli |
| Deadline | March 13, 2026 |
| Contact | ahmed.s.sow@aims-senegal.org|
---

## Project Description

This project aims to **predict the hourly demand for bike-sharing services** using historical data and weather conditions.

The objective is to build a **Deep Learning model** capable of estimating the number of bikes rented each hour.

Accurate predictions help to:

- Optimize bike distribution  
- Improve availability for users  
- Reduce operational costs  

---

## Problem Type

- Supervised Regression  
- Target variable: `count` → total number of bikes rented per hour

---

## Dataset

### Data Structure

1. **Train set (`train.csv`)**
   - Contains all features + the target variable `count`
   - Split into **training/validation** sets to evaluate model performance

2. **Validation set**
   - Part of the training data
   - Used to measure **RMSE** and prevent overfitting

3. **Test set (`test.csv`)**
   - Contains only the features, **without the target variable**
   - Used to generate final predictions

### Main Features

| Feature | Description |
|--------|-------------|
| datetime | date and time of the observation |
| season | season of the year |
| holiday | whether the day is a holiday |
| workingday | whether it is a working day |
| weather | weather condition |
| temp | actual temperature |
| atemp | perceived temperature |
| humidity | humidity level |
| windspeed | wind speed |

### Target Variable

| Variable | Description |
|------|-------------|
| count | total number of rented bikes |

---

## Data Preprocessing

1️⃣ **Feature Engineering**

- Extraction of `hour`, `weekday`, and `month` from `datetime` to capture daily and weekly patterns.

2️⃣ **One-Hot Encoding**

- Applied to categorical variables: season, holiday, workingday, weather, hour, weekday, month.

3️⃣ **Normalization**

- Applied to numerical variables: temp, humidity, windspeed.

4️⃣ **Logarithmic Transformation**


$y = log(1 + count)$


- Helps stabilize variance and improve model learning.

---

## Model – Deep Learning

- **Architecture**: Multi-Layer Perceptron (MLP)  
- **Framework**: PyTorch  
- **Activation Function**: ReLU  
- **Regularization**: Dropout  
- **Output Layer**: 1 neuron for regression

### Training

- Loss Function: MSE  
- Optimizer: Adam / SGD  
- Evaluation Metric: RMSE

---

## Model Evaluation

The model was evaluated on the **validation set**.

**Validation RMSE: < 80**

Tip: The RMSE can be further reduced by improving **feature engineering**, using **time-based validation**, or applying **hyperparameter optimization**.

---

## Challenge / Competition

You can participate by trying to improve the model or the pipeline:

- Better feature engineering  
- More advanced models (deep neural networks, etc.)  
- RMSE optimization  
- Time-based validation to simulate real-world scenarios

---

## Technologies

- Python  
- PyTorch  
- Pandas  
- NumPy  
- Scikit-learn  
- Matplotlib / Seaborn  

---

## Library Installation

To run this project, install the required libraries using Python 3.x:

```bash
# Install required libraries
pip install numpy pandas matplotlib seaborn scikit-learn torch
```

---

## Project Structure

```
bike_model_predict/
│
├── data/
│   ├── train.csv        # Training data with target variable
│   └── test.csv         # Test data without target variable
│
├── notebooks/
│   └── bike_model.ipynb   # Notebook containing the full pipeline
│
├── models/
│   └── baseline_model.pth        # Saved trained model
│
├── submission/
│   └── submission.csv   # Prediction file ready for submission
│
└── README.md            # This README file
```

## Submision
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://deeplearnigchallenge-9shfqyiumwvcerzjwy6tvw.streamlit.app/)
