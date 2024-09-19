# Machine Predictive Maintenance for Industrial Machines

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Machine Learning](https://img.shields.io/badge/Machine_Learning-blue?style=for-the-badge&logo=python&logoColor=ffdd54)
![scikit-learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Jupyter Notebook](https://img.shields.io/badge/jupyter-%23FA0F00.svg?style=for-the-badge&logo=jupyter&logoColor=white)
![Windows Terminal](https://img.shields.io/badge/Windows%20Terminal-%234D4D4D.svg?style=for-the-badge&logo=windows-terminal&logoColor=white)
![Shell Script](https://img.shields.io/badge/Bash-%23121011.svg?style=for-the-badge&logo=gnu-bash&logoColor=white)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)



## Download Repository

```
git clone https://github.com/Adhiban1/Machine-Predictive-Maintenance.git
```

## Change directory

```
cd Machine-Predictive-Maintenance
```

## Create virtual environment

```
python -m venv .venv
```

## Activate virtual environment

For windows
```
.venv/Scripts/activate 
```

For linux
```
source .venv/bin/activate
```

## Install requirements

```
pip install -r requirements.txt
```

## Train

Run `train.py` this will train the model and save the models into `models` folder

```
python myapp/modules/train.py
```

## Test

Run `test.py` to verify saved models work well

```
python myapp/modules/test.py
```

## App

Run web app

```
python manage.py runserver 5000
```

Dark mode:

![images/Screenshot4.png](images/Screenshot4.png)

Light mode:

![images/Screenshot5.png](images/Screenshot5.png)

Open it in browser `http://127.0.0.1:5000/`

