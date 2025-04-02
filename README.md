# emoji-stitcher
# 表情包拼接工具  Python脚本，用于横向或纵向拼接多个表情包/图片，支持重叠设置。  ## 功能 - 支持水平和垂直方向拼接 - 可自定义图片重叠像素数 - 保留透明背景(支持PNG)  ## 使用 ```python from stitch_emojis import stitch_emojis  # 示例 stitched = stitch_emojis(     ["img1.png", "img2.png"],     direction="horizontal",     overlap=20 ) stitched.save("output.png")
