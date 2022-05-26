#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# ## 2.1 Разбиение набора данных

# In[2]:


df=pd.read_csv('result_data.csv')


# Разобъём набор данных таким образом, как это рекомендовано согласно документации `Sklearn`. А именно `30 на 70`. Как представленно в описании, такая выборка является оптимальной, поскольку абсолютное большинство данных должно находится при обучении модели, чтобы получить наиболее оптимизированную модель со стороны её точности
# 
# ### Стратификация
# При разделении стратифицируем данные, чтобы получить одинаковую в процентом соотношении выборку, чтобы не было перевеса на какой-то один класс и такая ситуация не повлияла на некорректное обучение модели

# In[3]:


df


# In[4]:


df.replace([np.inf, -np.inf], np.nan, inplace=True)


# In[5]:


df=df[df['Rt']<5].reset_index(drop=True)


# ### Определение переменной опасности

# In[6]:


df1=df[df['Rt']<=0.7]
df1['Danger']=0


# In[7]:


df2=df[(df['Rt']>0.7) & (df['Rt']<=0.95)]
df2['Danger']=1


# In[8]:


df3=df[df['Rt']>0.95]
df3['Danger']=2


# In[9]:


df=pd.concat([df1, df2, df3]).reset_index(drop=True)


# In[10]:


X=df[['new_cases', 'new_deaths', 'Rt']]
y=df['Danger']


# In[11]:


#Получение выборок
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42, stratify=y)


# ## 2.3 Классифиткация 
# 
# Рассмотрим три модели классификации
# ### KNeighborsClassifier
# Классификация на основе соседей - это тип обучения на основе экземпляров или необобщающего обучения: он не пытается построить общую внутреннюю модель, а просто сохраняет экземпляры обучающих данных. Классификация вычисляется простым большинством голосов ближайших соседей каждой точки: точке запроса назначается класс данных, который имеет наибольшее количество представителей среди ближайших соседей точки.
# 
# ### RandomForestClassifier
# Случайный лес — это метаоценка, которая соответствует ряду классификаторов дерева решений для различных подвыборок набора данных и использует усреднение для повышения точности прогнозирования и контроля переобучения. Размер подвыборки управляется параметром max_samples, если bootstrap=True (по умолчанию), в противном случае для построения каждого дерева используется весь набор данных
# ### GaussianNB
# Наи́вный ба́йесовский классифика́тор — простой вероятностный классификатор, основанный на применении теоремы Байеса со строгими (наивными) предположениями о независимости. В зависимости от точной природы вероятностной модели, наивные байесовские классификаторы могут обучаться очень эффективно
# 
# ## Матрикики
# Рассмотрим две метрикики для оценивания модели классификации
# 
# ### accuracy f1-score
# Это гармоническое среднее значений точности и полноты. Возьмём её, потому что она дает лучшую оценку неправильно классифицированных случаев
# 
# ### macro avg f1-score
# 
# macro avg f1-score пожалуй, самый простой из многочисленных методов усреднения. Макроусредненная оценка F1 (или макрооценка F1) вычисляется путем взятия среднего арифметического (также известного как невзвешенное среднее) всех оценок F1 для каждого класса. Этот метод будет взят, поскольку он обрабатывает все классы одинаково, независимо от их значений поддержки

# ## 2.4 Обучение

# In[12]:


#Импорт моделей
from sklearn.metrics import classification_report
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB


# In[13]:


#Обучение
neigh = KNeighborsClassifier(n_neighbors=3)
neigh.fit(X_train, y_train)
preds=neigh.predict(X_test)
print(classification_report(preds, y_test))


# In[14]:


#Обучение
rfc = RandomForestClassifier()
rfc.fit(X_train, y_train)
rfc_preds=rfc.predict(X_test)
print(classification_report(rfc_preds, y_test))


# In[15]:


#Обучение
gnb = GaussianNB()
gnb.fit(X_train, y_train)
gnb_preds=gnb.predict(X_test)
print(classification_report(gnb_preds, y_test))


# ### Вывод
# Наиболее оптимальной моделью будет `KNeighborsClassifier` c accuracy f1-score = `0.78` и macro avg f1-score = `0.74`, поскольку по сравнению с другими он показал наилучший результат. `RandomForestClassifier` не будет взят, поскольку у него явное переобучение

# ## Отчёт
# * 2.1 Разбиение набора данных - набор данныхз разбит на обучаюшую и тестовую выборки
# * 2.3 Классификация - выбраны 3 алгоритма классификации
# * 2.4 Обучение - произведена классификация по уровню опасности

# In[ ]:


# Сохранение данных
df.to_csv('result_data.csv', encoding='utf-8-sig', index=False)

