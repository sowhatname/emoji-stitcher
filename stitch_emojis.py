from PIL import Image, ImageDraw, ImageFont
import platform  #用于获取与底层平台（操作系统、硬件等）相关的各种信息,如操作系统类型、硬件架构、Python 实现版本等。
import os
import math

# 获取系统默认表情符号字体的路径
def get_default_emoji_font_path():
    # 获取当前操作系统的名称
    system = platform.system()
    # 如果是 Windows 系统
    if system == "Windows":
        # 返回 Windows 系统下默认的表情符号字体路径
        return "C:/Windows/Fonts/seguiemj.ttf"
    # 如果是 macOS 系统
    elif system == "Darwin":
        # 返回 macOS 系统下默认的表情符号字体路径
        return "/System/Library/Fonts/Apple Color Emoji.ttc"
    # 对于其他系统（如 Linux）
    else:
        # 定义可能存在表情符号字体的路径列表
        possible_paths = [
            "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf",
            "/usr/share/fonts/opentype/noto/NotoColorEmoji.ttf",
        ]
        # 遍历可能的路径
        for path in possible_paths:
            # 检查路径是否存在
            if os.path.exists(path):
                # 如果存在，返回该路径
                return path
        # 如果都不存在，返回 None
        return None

# 渲染单个表情符号为图像
def render_emoji(emoji, font_size, emoji_size, font_path=None):
    # 如果没有指定字体路径
    if font_path is None:
        # 自动检测默认字体路径
        font_path = get_default_emoji_font_path()
        # 如果未找到默认字体路径
        if font_path is None:
            # 抛出异常提示用户指定字体路径
            raise ValueError("Could not find default emoji font. Please specify font_path.")

    # 尝试加载字体，支持 TTC/OTF 格式
    try:
        # 如果字体文件是 TTC 格式
        if font_path.endswith(".ttc"):
            # 加载 TTC 字体，索引为 0
            font = ImageFont.truetype(font_path, font_size, index=0)
        else:
            # 加载其他格式的字体
            font = ImageFont.truetype(font_path, font_size)
    # 如果加载字体失败
    except IOError:
        # 抛出异常提示无法从指定路径加载字体
        raise ValueError(f"Failed to load font from {font_path}")

    # 创建一个临时的 RGBA 图像，用于绘制表情符号 
    # 将画布大小设为 font_size * 2，确保渲染时有足够的空间，避免被意外裁剪。
    # color=(0, 0, 0, 0)表示透明背景
    temp_img = Image.new("RGBA", (font_size*2, font_size*2), (0, 0, 0, 0))
    # 创建一个 ImageDraw 对象，用于在临时图像上绘制
    draw = ImageDraw.Draw(temp_img)

    # 计算表情符号的边界框 返回四元组（left, top, right, bottom) 像素级边界框
    bbox = draw.textbbox((0, 0), emoji, font=font)
    # 计算表情符号的宽度 边界框右边界线坐标-左边
    text_width = bbox[2] - bbox[0]
    # 计算表情符号的高度 边界框下边界线坐标-上边
    text_height = bbox[3] - bbox[1]
    # 计算表情符号在临时图像中的水平位置  （画布宽度-实际图像宽度）/ 2 
    x = (temp_img.width - text_width) / 2 - bbox[0]
    # 计算表情符号在临时图像中的垂直位置
    y = (temp_img.height - text_height) / 2 - bbox[1]

    # 在临时图像上绘制表情符号，并支持颜色
    draw.text((x, y), emoji, font=font, embedded_color=True)

    # 调整临时图像的大小为指定的表情符号大小
    # Image.Resampling.LANCZOS 参数 指定图像缩放时使用的重采样算法
    # 保留边缘锐利度（避免模糊）减少彩色 Emoji 的颜色失真 计算量较大，但对小尺寸 Emoji 影响可忽略
    temp_img = temp_img.resize(emoji_size, Image.Resampling.LANCZOS)
    # 返回调整大小后的图像
    return temp_img

# 将多个表情符号拼接成一个图像
def stitch_emojis(emojis, direction="horizontal", overlap=20, 
                 font_size=100, emoji_size=(100, 100), font_path=None):
    # 用于存储每个表情符号渲染后的图像
    images = []
    # 遍历表情符号列表
    for emoji in emojis:
        # 调用 render_emoji 函数渲染单个表情符号
        img = render_emoji(emoji, font_size, emoji_size, font_path)
        # 将渲染后的图像添加到列表中
        images.append(img)

    # 计算最终拼接图像的大小
    if direction == "horizontal":
        # 计算水平拼接时的总宽度
        total_width = images[0].width + sum(img.width - overlap for img in images[1:])
        # 找到所有图像中的最大高度
        max_height = max(img.height for img in images)
        # 确定水平拼接时的画布大小
        canvas_size = (total_width, max_height)
    else:
        # 计算垂直拼接时的总高度
        total_height = images[0].height + sum(img.height - overlap for img in images[1:])
        # 找到所有图像中的最大宽度
        max_width = max(img.width for img in images)
        # 确定垂直拼接时的画布大小
        canvas_size = (max_width, total_height)

    # 创建一个透明的 RGBA 图像作为最终的拼接图像
    result = Image.new("RGBA", canvas_size, (0, 0, 0, 0))
    # 初始化水平和垂直位置
    x, y = 0, 0
    
    # 遍历渲染后的图像列表
    for i, img in enumerate(images):
        # 如果不是第一个图像
        if i > 0:
            if direction == "horizontal":
                # 水平拼接时，更新水平位置
                x += img.width - overlap
            else:
                # 垂直拼接时，更新垂直位置
                y += img.height - overlap
        # 将当前图像粘贴到最终图像上
        # 要粘贴的图像， 粘贴位置的左上角坐标， mask=img 透明部分保持透明
        result.paste(img, (x, y), img)
    
    # 返回拼接后的图像
    return result

if __name__ == "__main__":
    # 示例表情符号列表
    emojis = ["☝", "😮"]
    
    # 获取系统默认字体路径
    font_path = get_default_emoji_font_path()
    
    # 调用 stitch_emojis 函数生成拼接后的图片
    stitched_img = stitch_emojis(
        emojis,
        direction="horizontal",
        overlap=70,
        font_size=120,
        emoji_size=(128, 128),
        font_path=font_path
    )
    
    # 将拼接后的图片保存为 PNG 文件
    stitched_img.save("stitched_emojis.png")
