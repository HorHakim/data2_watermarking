from PIL import Image
import numpy

import string


def cesar_cipher(text, key, cipher):
	if type(text) == str and type(key) == int:
		shift = 1 if cipher else -1
		list_of_crypted_chars = []
		for char in text :
			list_of_crypted_chars.append(chr((ord(char) + shift * key) % 1_114_112))

		crypted_text = "".join(list_of_crypted_chars)
		return crypted_text
	else:
		raise(TypeError)


def hack_cesar_cipher(crypted_text, alphabet):
	if type(crypted_text) == str and type(alphabet) == str:
		for possible_key in range(0, 1_114_112):
			possible_uncryption = cesar_cipher(crypted_text, possible_key, cipher=False)
			if possible_uncryption[0] in alphabet:
				print(possible_key)
				print(possible_uncryption)
				print("_"*20)
	else:
		raise(TypeError)


def vigenere_cipher(text, password, cipher):
	list_of_crypted_chars = []
	list_of_keys = [ord(char) for char in password]
	
	for index, current_char in enumerate(text):
		
		current_key = list_of_keys[index % len(list_of_keys)]
		current_crypted_char = cesar_cipher(current_char, current_key, cipher)

		list_of_crypted_chars.append(current_crypted_char)

	crypted_text = "".join(list_of_crypted_chars)

	return crypted_text


def text_to_binary(text):
	list_binary_chars = []
	for char in text :
		list_binary_chars.append(bin(ord(char))[2:].zfill(21))

	binary_text = "".join(list_binary_chars)
	# Version Giga Chad
	# binary_text = "".join([bin(ord(char))[2:].zfill(21) for char in text]) 

	return binary_text



def display_image(image):
	image.show()







def watermark_lsb1(image_path, text):
	image = Image.open(image_path)
	image_array = numpy.array(image)
	even_image_array = image_array - image_array % 2

	binary_text = text_to_binary(text)


	original_image_shape = image_array.shape

	flatten_image_array = even_image_array.flatten()


	for index, bit in enumerate(binary_text):
		if bit == "1":
			flatten_image_array[index] += 1

	watermarked_image_array = flatten_image_array.reshape(original_image_shape)

	# watermarked_image = Image.fromarray(image_array, mode="RGB") # problème
	
	return watermarked_image_array



def get_text_from_watermarked_image(watermarked_image_array):
	# watermarked_image_array = numpy.array(watermarked_image)
	watermarked_flattened_image_array = watermarked_image_array.flatten()

	binary_text_array = watermarked_flattened_image_array % 2

	original_list_of_chars = []
	for index in range(0, len(binary_text_array), 21):
		current_binary_sequence = binary_text_array[index: index+21]

		current_binary_str = "".join([str(bit) for bit in current_binary_sequence])

		current_ordinal = int(current_binary_str, 2)
		if current_ordinal == 0:
			break

		current_char = chr(current_ordinal)
		original_list_of_chars.append(current_char)


	original_text = "".join(original_list_of_chars)
	return original_text


if __name__ == "__main__":
	message = "le chocolat est bon"

	# crypted_text = cesar_cipher(message, 12, cipher=True) # exo 1
	# print(crypted_text)

	# initial_message = cesar_cipher(crypted_text, 12, cipher=False) # exo 2
	# print(initial_message == message)

	# hack_cesar_cipher(crypted_text, alphabet=string.printable) # exo3

	# crypted_message = vigenere_cipher(text=message, password="Azerty12345!", cipher=True)
	# print(crypted_message)
	# initial_message = vigenere_cipher(text=crypted_message, password="Azerty12345!", cipher=False)
	# print(initial_message)

	# binary_text = text_to_binary(text=message)
	# print(binary_text)



	watermarked_image_array = watermark_lsb1("image.jpeg", text=message)
	original_text = get_text_from_watermarked_image(watermarked_image_array)
	print(original_text)