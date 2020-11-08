from PIL import Image
import argparse


parser = argparse.ArgumentParser(description="Melakukan Resize Image, diperlukan file image & target dimana file akan disimpan")
parser.add_argument('-f', '--file', type=str, required=True, help='directory dimana file foto yang akan diresize')
parser.add_argument('-t', '--target', type=str, required=True, help='directory dimana file hasil akan disimpan')
parser.add_argument('-s', '--scale', type=float, required=False, help='Opsional, nilai scale dari pixel photo dimana 0 < scale < 1')
parser.add_argument('-sz', '--size', type=str, required=False, help='Opsional, nilai fixed dari file baru, contoh 255,255 (dipisahkan dengan koma tanpa spasi)')

args = parser.parse_args()


def new_size(size, scale, sz):
    new_size = size
    if sz != None:
        sz = eval(sz)
        if type(sz) == tuple:
            if len(sz) == 2:
                new_size = sz
                return False, new_size
            else:
                return True, "Memerlukan 2 nilai (nilai_1, nilai_2) pada -sz"
        else:
            return True, "-sz memerlukan data seperti berikut: nilai_1,nilai_2"

    elif scale != None:
        if scale <= 0 or scale >= 1:
            return True, "scale memerlukan nilai 0 < scale < 1"
        point_1 = int(size[0]*scale)
        point_2 = int(size[1]*scale)
        new_size = (point_1, point_2)
        return False, new_size
    else:
        return False, new_size

if __name__ == "__main__":
    try:
        img = Image.open(args.file)
    except FileNotFoundError:
        print("Error: File: {} Not Found".format(args.file))
        exit()
    img_size = img.size
    is_err, new_size_val = new_size(img_size, args.scale, args.size)
    if is_err:
        print("Error resize image: {}".format(new_size_val))
        exit()
    print(new_size_val)
    new_image = img.resize(new_size_val, Image.ANTIALIAS)
    try:
        new_image.save(args.target, optimize=True, quality=75)
        new_image.close()
        img.close()
        print("Sukses menyimpan file dengan ukuran baru di: {}".format(args.target))
    except Exception as error:
        print("Gagal, pesan error: {}".format(error))

