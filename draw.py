from PIL import Image, ImageDraw
import hashlib
import glob

def sep_words(filename: str) -> dict:
	"""
	Take the MD5 hash of a file, then separate it into five words:
		1. four six-hexbit words and
		2. one eight-hexbit word.
	"""
	with open(filename, "rb") as fp:
		data = fp.read()
	s = hashlib.md5(data).hexdigest()	

	_d = {}
	for n in range(0, 4):
		_d[n + 1] = s[6*n : 6*(n + 1)]
	_d[5] = s[24:32]
	return _d
	

def make_im(filename: str, imsize: int = 600, central_sqsize: int = 450) -> Image:
	"""
	Apply sep_words to a file, then use the result to make a pretty picture.
	"""
	assert central_sqsize <= imsize, "Central square must fit inside the original image"
	imcoords = (imsize, imsize)
	sqsize = imsize // 2
	quads = {
		1: [sqsize, 0, imsize, sqsize],
		2: [0, 0, sqsize, sqsize],
		3: [0, sqsize, sqsize, imsize],
		4: [sqsize, sqsize, imsize, imsize]
	}
	csqsize = central_sqsize
	csqsize_half = csqsize // 2
	csq = [sqsize - csqsize_half, sqsize - csqsize_half, sqsize + csqsize_half, sqsize + csqsize_half]


	im = Image.new("RGBA", imcoords, color="#FFFFFFFF")
	dr = ImageDraw.Draw(im)
	words = sep_words(filename)
	for qn in range(1, 4+1):
		dr.rectangle(quads[qn], fill=f"#{words[qn]}")


	cim = Image.new("RGBA", imcoords, color="#FFFFFF00")
	cdr = ImageDraw.Draw(cim)
	cdr.rectangle(csq, fill=f"#{words[5]}")

	return Image.alpha_composite(im, cim)

if __name__ == "__main__":
	for f in glob.iglob("./*.pdf"):
		fstem = f[:-4]
		make_im(f).save(f"{fstem}.png")
