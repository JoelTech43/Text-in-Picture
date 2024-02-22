from PIL import Image

hex_dict = {'0':'0000','1':'0001','2':'0010','3':'0011','4':'0100','5':'0101','6':'0110','7':'0111','8':'1000','9':'1001','a':'1010','b':'1011','c':'1100','d':'1101','e':'1110','f':'1111'}

bin_dict = {'0000':'0','0001':'1','0010':'2','0011':'3','0100':'4','0101':'5','0110':'6','0111':'7','1000':'8','1001':'9','1010':'a','1011':'b','1100':'c','1101':'d','1110':'e','1111':'f'}

def toBin(a):
	a_bytes = bytes(a, 'ascii')
	binary = ''.join(bin(b)[2:].zfill(8) for b in a_bytes)
	return binary

def toString(a):
	a_list = a.split(' ')
	string = ''
	for i in a_list:
		p = chr(int(i,2))
		string = string + p
	return string

def hexToRgb(value):
	value = value.lstrip('#')
	lv = len(value)
	return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


def rgbToHex(rgb):
	return '%02x%02x%02x' % rgb

def Encrypt(imageFile):
	message = input('Enter message: ')
	print(len(message))
	print(len(message)*8)
	binary = toBin(message)
	print(len(binary))
	print(binary)
	n = 2
	binaryList = [binary[i:i+n] for i in range(0, len(binary), n)]
	print(binaryList)
	length = len(binaryList)-1
	print(length)
	x = 0
	
	input_image = Image.open(imageFile) 
	pixel_map = input_image.load() 
	width, height = input_image.size
	
	for i in range(height): 
		for j in range(width):
			r, g, b = input_image.getpixel((j, i)) 
			if x <= length:
				hex = rgbToHex((r, g, b))
				print("old rgb:", str(r), str(g), str(b))
				print("old hex: %s" % hex)
				blueBin = hex_dict[hex[5]]
				print("old blueBin: %s"%blueBin)
				blueBin2 = blueBin[:2] + binaryList[x]
				print("new blueBin: %s"%blueBin2)
				hex2 = hex[:5]+bin_dict[blueBin2]
				print("new hex: %s"%hex2)
				c = hexToRgb(hex2)
				r = c[0]
				g = c[1]
				b = c[2]
				print("new rgb:", str(r), str(g), str(b))
				x += 1
			else:
				pass
			pixel_map[j, i] = (r, g, b) 
	
	input_image.save("encrypt.png", format="png")

def Decrypt(imageFile):
	input_image = Image.open(imageFile) 
	pixel_map = input_image.load() 
	width, height = input_image.size
	messageList = []
	
	for i in range(height): 
		for j in range(width):
			r, g, b = input_image.getpixel((j, i)) 
			hex = rgbToHex((r, g, b))
			blueBin = hex_dict[hex[5]]
			messageList.append(str(blueBin[2:]))
			pixel_map[j, i] = (r, g, b)
	fullList = ''.join(messageList)
	n = 8
	finalMessage = []
	message = [fullList[i:i+n] for i in range(0, len(fullList), n)]
	print(message)
	print("\n")
	for item in message:
		finalMessage.append(toString(item))
	finalMessage = ''.join(finalMessage)
	
	print('Your message is: %s \n The end may look garbled. If it is, the message didn\'t fill all the image\'s pixels. Just ignore it!' % finalMessage)

Decrypt("encrypt.png")