from dataset import Dataset, Data_Loader
from model import Model
from Linear import Dense
from optim import GradientDecent, MomentumGD,  Adam, StepLR
from activations import ReLU,Sigmoid
from loss import CrossEntropyLoss
from utils import save_weights, load_weights

import time

# wieghts path
path = "ray2_weights.sav"


# MNIST Dataset
batch_size = 32
dataset = Dataset("train.csv")
dataloader = Data_Loader(dataset, batch_size)


model = Model()
model.add(Dense(784, 90))
model.add(ReLU())
model.add(Dense(90, 45))
model.add(ReLU())
model.add(Dense(45, 10))

model.set_loss(CrossEntropyLoss())

# optimizer = GradientDecent(model.parameters(), learning_rate = 0.01)
# optimizer = MomentumGD(model.parameters(), learning_rate = 0.01)
optimizer = Adam(model.parameters(), learning_rate = 0.01)
lr_schedular = StepLR(optimizer, step_size = 1, gamma=0.1)

model = load_weights(path)

epochs = 1
for epoch in range(epochs):
    i = 0
    for image, label in dataloader:
        # if i == 1700:
        #     break
        image = image/255
        i = i + 1
        print("Iteration no.", i)
        predicted = model(image)
        loss = model.loss(predicted, label)
        # model.backward()
        # optimizer.step()
        # print("loss= ", loss)
        # time.sleep(0.1)
        print("===========")

# save_weights(model, path)
