from PIL import Image


if __name__ == "__main__":
    ENCODE, DECODE, JPEG = range(1, 4)
    action = int(input("Encode, decode or transform to jpeg?\n1 - Encode\n2 - Decode\n3 - JPEG\n?: ") or ENCODE)

    if action == ENCODE:
        encode_image_path = input("Enter path to image you want to encode [img.bmp]: ") or "img.bmp"
        output_filename = ".".join(encode_image_path.split('.')[:-1]) + '.rle'

        print("Output file: %s" % (output_filename, ))
        img = Image.open(encode_image_path)
        data = list(img.getdata(0))

        print("Data size: %s" % (len(data), ))
        print("Data: %s" % (data, ))
        print("size per pixel: %s" % (len(data) / (img.width * img.height), ))
        print("f: %s m: %s" % (img.format, img.mode, ))

        width, height = img.width, img.height

        output_file = open(output_filename, 'w')

        output_file.write(
            '%s,%s,%s,%s,' % (img.format, img.mode, width, height, ))

        cnt = 1
        prev = data[0]
        for pixel in data[1:]:
            if prev != pixel:
                output_file.write("%s,%s," % (cnt, prev, ))
                prev = pixel
                cnt = 1
            else:
                cnt += 1
        output_file.write("%s,%s" % (cnt, pixel, ))
        output_file.close()

        # encImg = _encodeImage4bit(data, img.width, img.height)

    elif action == DECODE:
        decode_image_path = input("Enter path to image you want to decode [img.rle]: ") or "img.rle"
        output_filename = 'res_' + '.'.join(decode_image_path.split('.')[:-1]) + '.bmp'

        input_file = open(decode_image_path, 'r')

        def get_value(fd):
            res = []
            while True:
                c = fd.read(1)
                if c == ',' or not c: return ''.join(res)
                res.append(c)

        iformat, imode, width, height = (get_value(input_file) for _ in range(4))
        width = int(width)
        height = int(height)

        out_img = Image.new(mode=imode, size=(width, height))

        def get_pair():
            first = get_value(input_file)
            if not first: return None
            second = get_value(input_file)
            if not second: return None
            return first, second

        data = []
        for cnt, color in iter(get_pair, None):
            print("%s,%s" % (cnt, color, ))
            data.extend([int(color), ] * int(cnt))

        out_img.putdata(data)
        with open(output_filename, 'wb') as f:
            out_img.save(f, format=iformat)

        input_file.close()

    elif action == JPEG:
        encode_image_path = input("Enter path to image you want to encode [img.bmp]: ") or "img.bmp"
        output_filename = ".".join(encode_image_path.split('.')[:-1]) + '.jpg'

        YES_POOL = {'yes', 'y'}
        NO_POOL = {'no', 'n'}

        def get_bool(msg, default=True):
            ans = input(msg).lower()
            if ans in YES_POOL:
                return True
            elif ans in NO_POOL:
                return False
            else:
                return default

        quality = int(input("Enter quality [1-95]: ") or 75)
        if quality < 1:
            quality = 1
            print("Out of bound. Will be %s" % (quality, ))
        elif quality > 95:
            quality = 95
            print("Out of bound. Will be %s" % (quality, ))

        optimize = get_bool("Optimize? ", True)
        progressive = get_bool("Progressive? ", True)

        img = Image.open(encode_image_path)

        img.convert('RGB').save(output_filename, "JPEG", quality=quality,
                                optimize=optimize, progressive=progressive)

        print("Done!")
    else:
        print("Wrong action!")
