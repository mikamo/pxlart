from pxlart import PxlArt


image = PxlArt('test_image.jpg', 'output.png')

# decrease the size by dividing height and width by 4
image.resize(-4)

# get 10 most common colors
image.extract_color_palette(10)

# convert each pixel color to the closest one from the palette
image.assign_colors()

# convert each pixel color to the most common color in the neighborhood
# iterate 12 times and rotate picture after each iteration
image.combine_pxls(12)

# increase the size by multiplying height and width by 4
image.resize(4)

image.save_image()
