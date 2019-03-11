import io

import imageio


class Animation:
    def __init__(self, filename, duration=1, endpause=20, reverse=False):
        self._frames = []
        self.filename = filename
        self.duration = duration
        self.endpause = endpause
        self.reverse = reverse

    @property
    def frames(self):
        return self._frames

    @frames.setter
    def frames(self, img):
        with io.BytesIO() as output:
            img.save(output, format="GIF", quality=30)
            self._frames.append(output.getvalue())

    def save_gif(self):
        images = [imageio.imread(f) for f in self._frames]
        images += [images[-1] for _ in range(self.endpause)]

        if self.reverse:
            rrw = images.copy()
            rrw.reverse()
            images += rrw

        imageio.mimsave(self.filename, images, duration=self.duration)
