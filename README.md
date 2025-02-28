# 2D to Spatial Photo Converter

This tool converts standard 2D photos into spatial (3D) images by generating depth maps, creating stereoscopic left and right views, and packaging them into a side-by-side HEVC format compatible with spatial viewing devices.

## Overview

The 2D to Spatial Photo Converter uses machine learning to estimate depth from a single 2D image, then creates stereoscopic pairs with appropriate parallax to simulate a 3D effect. The process involves:

1. Depth map generation using the Depth-Anything-V2 model
2. Creating left and right stereoscopic views by shifting pixels based on the depth map
3. Inpainting missing areas caused by the shift operation
4. Combining the stereo images into a side-by-side HEVC container

## Requirements

- Python 3.8+
- PyTorch
- Transformers
- PIL (Pillow)
- NumPy
- SciPy
- OpenCV (cv2)
- FFmpeg (must be installed on your system)

Install the required Python packages with:

```bash
pip install -r requirements.txt
```

## Installation

1. Clone this repository:
```bash
git clone https://github.com/PRASHANT-tech870/spatial-photo-expansion.git
cd spatial-photo-expansion
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Ensure FFmpeg is installed on your system:
   - For Ubuntu/Debian: `sudo apt-get install ffmpeg`
   - For macOS: `brew install ffmpeg`
   - For Windows: [Download FFmpeg](https://ffmpeg.org/download.html)

## Usage

Run the converter on a single image:

```bash
python main.py --photo /path/to/your/image.jpg
```

The script will:
1. Create a random directory in the same location as your input image
2. Generate and save a depth map as `depth_image.jpg`
3. Create left and right stereo images as `stereo_left.png` and `stereo_right.png`
4. Combine them into an HEVC file named `output.hevc`

## How It Works

### 1. FileMixin (`file_mixin.py`)

This utility class manages the creation of a random directory to store output files. It generates a folder with a random name in the same directory as the input image.

### 2. ImageHandler (`image_handler.py`)

The main class that processes the image through these steps:

#### Depth Map Generation
- Uses Hugging Face's `transformers` pipeline with the "Depth-Anything-V2-large-hf" model
- Processes the input image to estimate depth at each pixel
- Saves the depth map as a grayscale image

#### Stereoscopic Image Creation
- Creates left and right views by shifting pixels based on the depth information
- Pixels representing objects closer to the viewer (brighter in depth map) are shifted more than distant objects
- Different shift amounts are applied for left (10px) and right (50px) images to create the stereo effect

#### Inpainting
- The shifting process creates empty areas where information is missing
- Uses OpenCV's inpainting algorithm to fill in these gaps with plausible content
- Produces clean stereo pairs without visual artifacts

#### HEVC Encoding
- Uses FFmpeg to combine the left and right images into a side-by-side HEVC format
- Creates a single output file that can be viewed on spatial photo viewers

### 3. Main Script (`main.py`)

The entry point that:
- Sets up environment variables for hardware acceleration
- Parses command-line arguments
- Initializes the ImageHandler with the input photo
- Triggers the conversion process

## Output Files

In the randomly generated directory, you'll find:
- `depth_image.jpg`: The estimated depth map
- `stereo_left.png`: The left-eye view
- `stereo_right.png`: The right-eye view
- `output.hevc`: The final side-by-side HEVC file

## Customization

- Modify the shift amounts (currently 10 for left and 50 for right) in `make_3d_image()` to adjust the 3D effect intensity
- Change the depth estimation model by updating the pipeline configuration in `generate_depth_image()`
- Uncomment the CUDA lines to enable GPU acceleration if you have an NVIDIA GPU

## Notes

- Processing time depends on the image size and your hardware
- Depth estimation runs on CPU by default but can be accelerated with CUDA (GPU) by uncommenting the relevant lines
- The quality of the 3D effect depends on the accuracy of the depth estimation, which works best with clear foreground/background separation


## Acknowledgments

- The image shifting algorithm is adapted from [DamnGoodTech's method](https://medium.com/@damngoodtech/creating-3d-stereo-images-from-2d-images-using-invokeai-4245902abef5)
- Depth estimation powered by [Depth-Anything-V2](https://huggingface.co/docs/transformers/main/en/model_doc/depth_anything_v2) from Hugging Face
