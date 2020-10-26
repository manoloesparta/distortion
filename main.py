from neuraln import NeuralNetwork

def main():
	
	# Create neural network
	ann = NeuralNetwork(data_path='./dataset')

	# Traine it
	ann.train(1)

	# Try it out
	ann.predict('prueba.wav')

if __name__ == '__main__':
	main()