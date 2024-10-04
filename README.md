# HOW TO RUN DASHBOARD

## Setup Environment - Anaconda
```
conda create --name env-juna python=3.10
conda activate env-juna
pip install -r requirements.txt
```

## Setup Environment - Shell/Terminal
```
mkdir analisis_data_dicoding
cd analisis_data_dicoding
pipenv install
pipenv shell
pip install -r requirements.txt
```

## Run steamlit app
```
streamlit run dashboard.py
```