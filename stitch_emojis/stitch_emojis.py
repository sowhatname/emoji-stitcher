from PIL import Image
import math


def stitch_emojis(image_paths, direction="horizontal", overlap=20):
    # 路径列表 排列方向（横、纵） 重叠像素数（默认20）

    images = [Image.open(path).convert("RGBA") for path in image_paths]

    total_width = 0

    if direction == "horizontal":
        total_width = images[0].width + sum(img.width - overlap for img in images[1:])
        max_height = max(img.height for img in images)
        new_img_size = (total_width, max_height)

    else:
        max_width = max(img.width for img in images)
        total_height = images[0].height + sum(img.height - overlap for img in images[1:])
        new_img_size = (max_width, total_height)

    new_img = Image.new("RGBA", new_img_size, (0, 0, 0, 0))  #空白新图片透明背景

    #粘贴
    x, y = 0, 0
    for i, img in enumerate(images):

        #计算重叠位置
        if i > 0:  #第一张直接粘 跳过
            if direction == "horizontal":
                x += img.width - overlap
            else:
                y += img.height - overlap
        
        new_img.paste(img, (x, y), img)

    return new_img

if __name__ == "__main__":
    images =["F:/Users/asus/Pictures/emojis/1.jpg", "F:/Users/asus/Pictures/emojis/5.jpg", "F:/Users/asus/Pictures/emojis/7.jpg"]
    stitched = stitch_emojis(images, direction="horizontal", overlap=40)

    stitched.save("F:/Users/asus/Pictures/emojis/stitched3.png")