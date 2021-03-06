#대충 짜보기만 했습니다
#4개 layer(hidden 2개), learning rate=0.001, training epoch =20, batch size =100
#각 레이어의 인풋과 아웃풋은 784->256->256->256->10
#cnn은 적용 아직 못했고요, 단순한 멀티 레이어입니다
#테스트 데이터에 라벨이 없어서 정확도를 (캐글에 올리기 전엔) 확인할 수 없기 때문에 training 데이터를 7:3으로 나눠서 검증했습니다.
#one_hot 함수는 직접 만들어서 썼고, 김성훈교수님꺼 많이 참고했습니다.
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  8 15:23:47 2018 
@author: kimseunghyuck(smallerhand)
"""
## 개선할 사항: layer수 늘리기, weight 초기값 xavier(오류나서 못했음), activation function 은 maxout을 쓰자. 
## dropout(앙상블). adam optimizer
import tensorflow as tf
import pandas as pd
import numpy as np
train = pd.read_csv('desktop/python/train.csv')
test = pd.read_csv('desktop/python/test.csv')
#훈련세트, validation세트 나누기
from sklearn.model_selection import train_test_split
train_set, validate_set = train_test_split(train, test_size = 0.3)
trainData = train_set.values[:,1:]
validateData = validate_set.values[:,1:]
#one hot function(n=10)
def one_hot(x):
    lst=[]
    for i in x:
        lst.append([0,0,0,0,0,0,0,0,0,0])
        lst[-1][i]+=1
    return(lst)
trainLabel=one_hot(train_set.values[:,0])
validateLabel=one_hot(validate_set.values[:,0])
# parameters
learning_rate = 0.002
training_epochs = 40
batch_size = 100
# input place holders
X = tf.placeholder(tf.float32, [None, 784])
Y = tf.placeholder(tf.float32, [None, 10])
# weights & bias for nn layers
W1 = tf.Variable(tf.random_normal([784, 256]))
b1 = tf.Variable(tf.random_normal([256]))
L1 = tf.nn.relu(tf.matmul(X, W1) + b1)

W2 = tf.Variable(tf.random_normal([256, 256]))
b2 = tf.Variable(tf.random_normal([256]))
L2 = tf.nn.relu(tf.matmul(L1, W2) + b2)

W3 = tf.Variable(tf.random_normal([256, 256]))
b3 = tf.Variable(tf.random_normal([256]))
L3 = tf.nn.relu(tf.matmul(L2, W3) + b3)

W4 = tf.Variable(tf.random_normal([256, 10]))
b4 = tf.Variable(tf.random_normal([10]))
hypothesis = tf.matmul(L3, W4) + b4

# define cost/loss & optimizer
cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(
    logits=hypothesis, labels=Y))
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)
# initialize 
sess = tf.Session()
sess.run(tf.global_variables_initializer())
# train my model
for epoch in range(training_epochs):
    avg_cost = 0
    total_batch = int(len(trainData) / batch_size)
    for i in range(total_batch):
        batch_xs = trainData[i*batch_size:(i+1)*batch_size]
        batch_ys = trainLabel[i*batch_size:(i+1)*batch_size]
        feed_dict = {X: batch_xs, Y: batch_ys}
        c, _ = sess.run([cost, optimizer], feed_dict=feed_dict)
        avg_cost += c / total_batch
    print('Epoch:', '%04d' % (epoch + 1), 'cost =', '{:.9f}'.format(avg_cost))
print('Learning Finished!')

# Test model and check accuracy(validation)
correct_prediction = tf.equal(tf.argmax(hypothesis, 1), tf.argmax(Y, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
print('Accuracy:', sess.run(accuracy, feed_dict={
      X: validateData, Y: validateLabel}))
    
#94~96퍼센트 정확도 나옴.