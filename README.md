# Image to Binvis.io

A python tool for hiding pixel art (or any data for that matter) in binary for binvis.io

## Usage

There are two main functions in this tool, `binary_to_img` and `img_to_binary`, and a few other helper functions.

This converts a given binary array with given offsets to an image. The output image should be consistent with the output from [bisvis.io](http://binvis.io).

Currently, only cluster + byteclass mode is implemented.

`img_to_binary` finds the differences between the original image output and the input image, and only changes bytes in the binary file that affect the concerned pixels. The bytes are changed into a random value that give the same color as specified by the input image. If the image pixel is the same as the original image, the byte is left unchanged.

Below is a simple example of how to use the tool:

```python
data = get_binary("path/to/file") # get binary data from file
offset_start = 0
offset_end = data.shape[0]
img = binary_to_img(data, offset_start, offset_end)

# save then show the image
cv.imwrite("reconstructed.png", img)
cv.imshow("image", img)

# you can now edit the image file, and then close the opencv window to use the edited file
cv.waitKey(0)

img = cv.imread("reconstructed.png").astype(np.uint8)
img_to_binary(img, "path/to/output", data, offset_start, offset_end)
```
