import random
import keras
from keras.layers import Input
from keras.models import Model

from keras.applications.resnet50 import preprocess_input, decode_predictions
import os
from PIL import Image
import numpy as np

# from tensorflow.compat.v1 import ConfigProto
# from tensorflow.compat.v1 import InteractiveSession

# config = ConfigProto()
# config.gpu_options.per_process_gpu_memory_fraction = 0.7
# config.gpu_options.allow_growth = True
# session = InteractiveSession(config=config)


height = 224
width = 224
# копирование изображений в массив нумпай и изменение их размеров
# попробуйте написать код, который сохраняет соотношение сторон
nh = 224
nw = 224
ncol = 3

visible2 = Input(shape=(nh, nw, ncol), name='imginp')
resnet = keras.applications.resnet_v2.ResNet50V2(include_top=True, weights='imagenet', input_tensor=visible2,
                                                 input_shape=None, pooling=None, classes=1000)


def read_image_files(files_max_count, dir_name):
    files = [item.name for item in os.scandir(dir_name) if item.is_file()]
    files_count = files_max_count

    if (files_max_count > len(files)):  # определяем количество файлов не больше max
        files_count = len(files)
    image_box = [[]] * files_count
    for file_i in range(files_count):  # читаем изображения в список
        image_box[file_i] = Image.open(dir_name + '/' + files[file_i]).convert("RGB")  # / ??

    return files_count, image_box


# x = preprocess_input(x)
def getresult(image_box):

    files_count = len(image_box)
    images_resized = [[]] * files_count
    for i in range(files_count):
        # Сохранение исходных размеров
        # x_im_size, y_im_size = image_box[i].size
        # ratio = x_im_size/y_im_size
        # new_width = width
        # new_height = int(ratio * height)
        images_resized[i] = np.array(image_box[i].resize(( height, width))) / 255.0
    images_resized = np.array(images_resized)
    out_net = resnet.predict(images_resized)
    decode = decode_predictions(out_net, top=1)
    return decode