# Nonlinear Parametric Model for Geodetic Survey

This repository contains a solution for a geodetic survey problem using a nonlinear parametric model, specifically for a 7-point geodetic network. The problem involves computing the coordinates of points using the least squares method, based on distance measurements obtained through an EDM (Electronic Distance Measurement) device. The solution is implemented in Python 2.7.

## Problem Overview

We are given a 7-point geodetic network where the coordinates of points 1 and 2 are fixed, and the approximate coordinates of the remaining points are provided. The distances between the points are measured independently using a TOPCON EDM device, with a precision of 2mm + 2ppm. The goal is to calculate the adjusted coordinates of the points using the least squares method. Other outputs such as residuals, adjusted observations, and covariance matrices are also included.

### Known Points:

| Point | X        | Y        |
|-------|----------|----------|
| 1     | 978.00   | 788.00   | (Fixed) |
| 2     | 978.00   | 865.00   | (Fixed) |
| 3     | 1045.00  | 827.00   |
| 4     | 1045.00  | 750.00   |
| 5     | 978.00   | 712.00   |
| 6     | 929.00   | 760.00   |
| 7     | 912.00   | 827.00   |

### Measured Distances Between Points:

| From | To  | Distance (m) |
|------|-----|--------------|
| 1    | 3   | 76.7544      |
| 1    | 4   | 76.8124      |
| 1    | 5   | 76.8884      |
| 1    | 6   | 56.2724      |
| 1    | 7   | 76.5964      |
| 2    | 3   | 76.8074      |
| 2    | 4   | 132.9404     |
| 2    | 5   | 153.5524     |
| 2    | 6   | 115.7274     |
| 2    | 7   | 76.5694      |
| 3    | 4   | 76.7504      |
| 3    | 5   | 133.0324     |
| 3    | 6   | 132.9864     |
| 3    | 7   | 132.7724     |
| 4    | 5   | 76.8814      |
| 4    | 6   | 115.5144     |
| 4    | 7   | 153.3614     |
| 5    | 6   | 68.6254      |
| 5    | 7   | 132.8914     |
| 6    | 7   | 69.0384      |

### Solution Approach

This code implements the solution to the problem using the **least squares method** to adjust the coordinates of the points based on the given distances. The adjustments are made iteratively until the residuals (differences between the observed and calculated distances) are minimized. Additional outputs like the adjusted observations and covariance matrices are also computed.

### Code Details

- **Language**: Python 2.7
- **Libraries**: The code uses standard Python libraries for numerical calculations and data handling.

## How to Use

1. **Import Coordinate File**: First, import the file containing the initial coordinates of the points.
2. **Import Distance File**: Next, import the file containing the distance measurements between the points.
3. **Run the Code**: The code will compute the adjusted coordinates of the points using the least squares method.

### Demo GIF

The following GIF demonstrates the user interface (GUI) for running the code:

![Geodetic Survey Nonlinear Parametric GUI](geodetic-survey/Geodetic_Survey_Nonlinear_parametric.gif)

In the demo:

- First, the coordinate file is imported.
- Then, the distance file is imported.
- The adjusted coordinates will be computed and displayed.

## Note

This solution is for educational purposes and was developed as part of a **Geodetic Survey** course practice. The code demonstrates the use of nonlinear parametric models and least squares adjustment techniques in geodetic surveying.

