import numpy as np
from PIL import Image

WIDTH = 1024
HEIGHT = 1024


class Point:
    def __init__(self, x, y):
        self.x = y
        self.y = x

    def distance(self, otherPoint):
        dx = self.x - otherPoint.x
        dy = self.y - otherPoint.y
        return np.sqrt(dx ** 2 + dy ** 2)

    def __str__(self):
        return f'(( {self.x:6.2f} , {self.y: 6.2f}))'


class Wave:
    def __init__(self, center, amplitude, wavelength, phase):
        self.center = center
        self.amplitude = amplitude
        self.wavelength = wavelength
        self.phase = phase

    def height(self, point):
        r = point.distance(self.center)
        angle = 2.0 * np.pi * r / self.wavelength + self.phase
        return self.amplitude * np.sin(angle)


class InterferingWaves:
    def __init__(self):
        self.waves = list()

    def addWave(self, wave):
        self.waves.append(wave)

    def height(self, point):
        sum = 0.0

        for wave in self.waves:
            sum += wave.height(point)

            return sum


class CoordinateSystem:
    def __init__(self, xMin, yMin, xMax, yMax):
        self.xMin = xMin
        self.yMin = yMin

        self.xMax = yMax
        self.yMax = yMax

    def normalize(self, point):
        x = (point.x - self.xMin) / (self.xMax - self.xMin)
        y = (point.y - self.yMin) / (self.yMax - self.yMin)

        return Point(x, y)

    def scaleAndTranslate(self, point):
        x = self.xMin + point.x * (self.xMax - self.xMin)
        y = self.yMin + point.y * (self.yMax - self.yMin)

        return Point(x, y)


class Transform:
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination

    def map(self, point):
        n = self.source.normalize(point)

        return self.destination.scaleAndTranslate(n)


def normalize(values):
    minimum = values.min()
    maximum = values.max()

    fun = lambda x: 256 * (x - minimum) / (maximum - minimum)

    return fun(values)


def main():
    print("Guten_Tag!")


amplitudes = np.zeros((WIDTH, HEIGHT))

world = CoordinateSystem(-1.0, -1.0, +1.0, + 1.0)

device = CoordinateSystem(0, 0, WIDTH, HEIGHT)

device2world = Transform(device, world)

pattern = InterferingWaves()

numberOfWaves = 4

radius = 0.4

cx = 0.0

cy = 0.0

for k in range(numberOfWaves):
    angle = 2.0 * np.pi * k / numberOfWaves
    x = cx + radius * np.cos(angle)
    y = cy + radius * np.sin(angle)

    center = Point(x, y)

    wave = Wave(center, 1.0, 0.2, 0.0)

    pattern.addWave(wave)

for row in range(HEIGHT):
    for column in range(WIDTH):
        u = Point(column, row)
        v = device2world.map(u)

        h = pattern.height(v)
        amplitudes[row, column] = h

normalizedAmplitudes = normalize(amplitudes).astype(np.uint8)

print(normalizedAmplitudes.dtype)

image = Image.fromarray(normalizedAmplitudes, "L")
image.show()

if __name__ == '__main__':
    main()
