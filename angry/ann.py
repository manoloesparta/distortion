import numpy as np
from tqdm import tqdm
import librosa.display
from angry import load
import os, shutil, librosa
from pydub import AudioSegment
from angry import NeuralNetwork
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split


class AngryNeuralNetwork():


	def __init__(self, data_path):
		self.data_path = data_path
		self.model = NeuralNetwork()
		self.model.compile(optimizer='adam', loss='mse', metrics=['mse'])


	def train(self, epochs=10):
		x, y = load.load_dataset(self.data_path)
		x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1)
		
		self.model.fit(x_train, y_train, epochs=epochs, validation_data=(x_test, y_test), shuffle=False)
		test_loss, test_acc = self.model.evaluate(x_test, y_test, verbose=1) 

		print(f'Test accuracy: {test_acc}, Test loss: {test_loss}')


	def predict_clip(self, file_path, output='output', remove=False):
		if os.path.exists('tmp'):
			shutil.rmtree('tmp')
		os.mkdir('tmp')

		arr = []
		audio = AudioSegment.from_file(file_path, 'wav')

		for i in range(0, len(audio) - 500, 500):
			audio_slice = audio[i:i+500]
			audio_slice.export(f'tmp/audio{i//500}.wav',format='wav')
			y, sr = librosa.load(f'tmp/audio{i//500}.wav')
			arr.append(librosa.feature.melspectrogram(y=y, sr=sr))

		res = self.model.predict(np.array(arr))

		shutil.rmtree('tmp')
		os.mkdir('tmp')

		for i, val in enumerate(tqdm(res)):
			audio = librosa.feature.inverse.mel_to_audio(val)
			librosa.output.write_wav(f'tmp/{output}{i}.wav', audio, sr=22050)

		final = AudioSegment.empty()
		for i, _ in enumerate(res):
			final += AudioSegment.from_wav(f'tmp/{output}{i}.wav')

		final.export(f'{output}.wav', format='wav')

		if remove:
			shutil.rmtree('tmp')
