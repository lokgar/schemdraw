import math
import random
from typing import Sequence, Tuple

import schemdraw
import schemdraw.elements
from schemdraw import dsp

from schemdraw.elements import Element
from schemdraw.segments import Segment, SegmentArc, SegmentCircle, SegmentPoly


OPTCOL = "#1f77b4"
RFCOL = "#d62728"
ELCOL = "#000000"


class Rectangle(Element):
    def __init__(self, width=1.85, height=1.25, **kwargs):
        super().__init__(**kwargs)
        self.width = width
        self.height = height
        self.segments.append(
            SegmentPoly(
                [
                    (0, -self.height / 2),
                    (self.width, -self.height / 2),
                    (self.width, self.height / 2),
                    (0, self.height / 2),
                    (0, -self.height / 2),
                ]
            )
        )
        self.elmparams["lblloc"] = "center"
        self.elmparams["lblofst"] = 0

        self.anchors["N"] = (self.width / 2, self.height / 2)
        self.anchors["S"] = (self.width / 2, -self.height / 2)
        self.anchors["E"] = (self.width, 0)
        self.anchors["W"] = (0, 0)
        self.elmparams["drop"] = self.anchors["E"]


class Fiber(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.radius = 0.3
        self.length = 1.5
        self.segments.append(Segment([(0, 0), (self.length, 0)]))
        self.segments.append(
            SegmentCircle((self.length / 2 - 0.1, self.radius), self.radius, fill=False)
        )
        self.segments.append(
            SegmentCircle((self.length / 2 + 0.1, self.radius), self.radius, fill=False)
        )

        self.elmparams["drop"] = (self.length, 0)


class PolCtrl(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.radius = 0.15
        self.length = 1
        self.segments.append(Segment([(0, 0), (self.length, 0)]))
        self.segments.append(
            SegmentCircle(
                (self.length / 2 - 2 * self.radius, self.radius),
                self.radius,
                fill=False,
            )
        )
        self.segments.append(
            SegmentCircle((self.length / 2, self.radius), self.radius, fill=False)
        )
        self.segments.append(
            SegmentCircle(
                (self.length / 2 + 2 * self.radius, self.radius),
                self.radius,
                fill=False,
            )
        )
        self.elmparams["drop"] = (self.length, 0)


class VOA(Rectangle):
    def __init__(self, width=1, height=1, **kwargs):
        super().__init__(width=width, height=height, **kwargs)
        self.width = width
        self.height = height

        self.segments.append(
            SegmentCircle((self.width / 2, 0), self.width / 2 - 0.2, fill=False)
        )

        x_ofst = 0.17
        y_ofst = 0.17

        self.segments.append(
            Segment(
                [
                    (0.0 + x_ofst, -self.height / 2 + y_ofst),
                    (0.7 + x_ofst, 0.2 + y_ofst),
                ],
                arrow="->",
                arrowlength=0.15,
                arrowwidth=0.1,
            )
        )


class Mod(Rectangle):
    def __init__(self, width=1.5, height=1.0, **kwargs):
        super().__init__(width, height, **kwargs)

        self.segments.append(Segment([(0.1, 0), (0.2, 0)]))
        self.segments.append(Segment([(0.2, 0), (0.4, 0.2)]))
        self.segments.append(Segment([(0.4, 0.2), (1.1, 0.2)]))
        self.segments.append(Segment([(1.1, 0.2), (1.3, 0)]))
        self.segments.append(Segment([(1.3, 0), (1.4, 0)]))
        self.segments.append(Segment([(0.2, 0), (0.4, -0.2)]))
        self.segments.append(Segment([(0.4, -0.2), (1.1, -0.2)]))
        self.segments.append(Segment([(1.1, -0.2), (1.3, 0)]))

        self.segments.append(
            SegmentPoly([(0.4, 0.3), (0.4, 0.35), (1.1, 0.35), (1.1, 0.3)], fill=True)
        )
        self.segments.append(
            SegmentPoly(
                [(0.4, -0.3), (0.4, -0.35), (1.1, -0.35), (1.1, -0.3)], fill=True
            )
        )
        self.segments.append(
            SegmentPoly([(0.4, -0.1), (0.4, 0.1), (1.1, 0.1), (1.1, -0.1)], fill=True)
        )


class OSA(Rectangle):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Disaplay inside the screen
        disp_x_offset = 0.2
        disp_y_offset = -0.35
        disp_width = 1.1
        disp_height = 0.7

        self.segments.append(
            SegmentPoly(
                [
                    (disp_x_offset, disp_y_offset + disp_height),
                    (
                        disp_x_offset + disp_width,
                        disp_y_offset + disp_height,
                    ),
                    (disp_x_offset + disp_width, disp_y_offset),
                    (disp_x_offset, disp_y_offset),
                ],
                cornerradius=0.25,
            )
        )

        # Large knob on the right
        self.segments.append(SegmentCircle((1.6, 0.35), 0.1, fill=False))

        # Rectangular buttons
        button_width = 0.1
        button_height = 0.1
        button_x_offset = 1.55
        button_y_offset = -0.5
        button_spacing = 0.1

        self.segments.extend(
            SegmentPoly(
                [
                    (
                        button_x_offset,
                        button_y_offset + i * (button_height + button_spacing),
                    ),
                    (
                        button_x_offset + button_width,
                        button_y_offset + i * (button_height + button_spacing),
                    ),
                    (
                        button_x_offset + button_width,
                        button_y_offset
                        + i * (button_height + button_spacing)
                        + button_height,
                    ),
                    (
                        button_x_offset,
                        button_y_offset
                        + i * (button_height + button_spacing)
                        + button_height,
                    ),
                ],
                fill=False,
            )
            for i in range(3)
        )

        # Spectrum on the screen
        def _make_spectrum(
            length: int = 150,
        ) -> Sequence[Tuple[float, float]]:
            path = []
            for x in range(length):
                if length // 2 - 5 < x < length // 2 + 5:
                    y = 0.8 * disp_height * (1 - abs(x - length // 2) / 5)
                else:
                    y = 0.2 * disp_height * (random.random() - 0.5)
                path.append((x / length * 0.8 * disp_width, 0.8 * y))
            return path

        path = _make_spectrum()
        path = [
            (x + disp_x_offset + 0.1 * disp_width, y + disp_y_offset + 0.15)
            for x, y in path
        ]
        self.segments.append(Segment(path))


class ESA(Rectangle):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Disaplay inside the screen
        disp_x_offset = 0.2
        disp_y_offset = -0.35
        disp_width = 1.1
        disp_height = 0.7

        self.segments.append(
            SegmentPoly(
                [
                    (disp_x_offset, disp_y_offset + disp_height),
                    (
                        disp_x_offset + disp_width,
                        disp_y_offset + disp_height,
                    ),
                    (disp_x_offset + disp_width, disp_y_offset),
                    (disp_x_offset, disp_y_offset),
                ],
                cornerradius=0.25,
            )
        )

        # Large knob on the right
        self.segments.append(SegmentCircle((1.6, 0.35), 0.1, fill=False))

        # Rectangular buttons
        button_width = 0.1
        button_height = 0.1
        button_x_offset = 1.55
        button_y_offset = -0.5
        button_spacing = 0.1

        self.segments.extend(
            SegmentPoly(
                [
                    (
                        button_x_offset,
                        button_y_offset + i * (button_height + button_spacing),
                    ),
                    (
                        button_x_offset + button_width,
                        button_y_offset + i * (button_height + button_spacing),
                    ),
                    (
                        button_x_offset + button_width,
                        button_y_offset
                        + i * (button_height + button_spacing)
                        + button_height,
                    ),
                    (
                        button_x_offset,
                        button_y_offset
                        + i * (button_height + button_spacing)
                        + button_height,
                    ),
                ],
                fill=False,
            )
            for i in range(3)
        )

        # Spectrum on the screen
        def _make_spectrum(
            length: int = 200,
        ) -> Sequence[Tuple[float, float]]:
            path = []
            peaks = [length // 4, length // 2, 3 * length // 4]
            amplitudes = [0.5, 0.7, 0.5]
            for x in range(length):
                y = 0
                for peak, amplitude in zip(peaks, amplitudes):
                    if peak - 5 < x < peak + 5:
                        y += amplitude * disp_height * (1 - abs(x - peak) / 5)
                    else:
                        y += 0.08 * disp_height * (random.random() - 0.5)
                path.append((x / length * 0.8 * disp_width, 0.9 * y))
            return path

        path = _make_spectrum()
        path = [
            (
                x + disp_x_offset + 0.1 * disp_width,
                y + disp_y_offset + 0.15,
            )
            for x, y in path
        ]
        self.segments.append(Segment(path))


class AWG(Rectangle):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Disaplay inside the screen
        disp_x_offset = 0.2
        disp_y_offset = -0.35
        disp_width = 1.1
        disp_height = 0.7

        self.segments.append(
            SegmentPoly(
                [
                    (disp_x_offset, disp_y_offset + disp_height),
                    (
                        disp_x_offset + disp_width,
                        disp_y_offset + disp_height,
                    ),
                    (disp_x_offset + disp_width, disp_y_offset),
                    (disp_x_offset, disp_y_offset),
                ],
                cornerradius=0.25,
            )
        )

        # Large knob on the right
        self.segments.append(SegmentCircle((1.6, 0.35), 0.1, fill=False))

        # Rectangular buttons
        button_width = 0.1
        button_height = 0.1
        button_x_offset = 1.55
        button_y_offset = -0.5
        button_spacing = 0.1

        self.segments.extend(
            SegmentPoly(
                [
                    (
                        button_x_offset,
                        button_y_offset + i * (button_height + button_spacing),
                    ),
                    (
                        button_x_offset + button_width,
                        button_y_offset + i * (button_height + button_spacing),
                    ),
                    (
                        button_x_offset + button_width,
                        button_y_offset
                        + i * (button_height + button_spacing)
                        + button_height,
                    ),
                    (
                        button_x_offset,
                        button_y_offset
                        + i * (button_height + button_spacing)
                        + button_height,
                    ),
                ],
                fill=False,
            )
            for i in range(3)
        )

        # Waveform on the screen
        def _make_sum_of_sines(
            length: int = 500,
        ) -> Sequence[Tuple[float, float]]:
            path = []
            for x in range(length):
                y = (
                    0.2 * disp_height * math.sin(5 * math.pi * x / length)
                    + 0.2 * disp_height * math.sin(10 * math.pi * x / length)
                    + 0.4 * disp_height * math.sin(15 * math.pi * x / length)
                )
                path.append((x / length * 0.8 * disp_width, 0.45 * y))
            return path

        path = _make_sum_of_sines()
        path = [
            (
                x + disp_x_offset + 0.1 * disp_width,
                y + disp_y_offset + disp_height / 2.1,
            )
            for x, y in path
        ]
        self.segments.append(SegmentPoly(path, fill=True))


class Scope(Rectangle):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Disaplay inside the screen
        disp_x_offset = 0.2
        disp_y_offset = -0.35
        disp_width = 1.1
        disp_height = 0.7

        self.segments.append(
            SegmentPoly(
                [
                    (disp_x_offset, disp_y_offset + disp_height),
                    (
                        disp_x_offset + disp_width,
                        disp_y_offset + disp_height,
                    ),
                    (disp_x_offset + disp_width, disp_y_offset),
                    (disp_x_offset, disp_y_offset),
                ],
                cornerradius=0.25,
            )
        )

        # Large knob on the right
        self.segments.append(SegmentCircle((1.6, 0.35), 0.1, fill=False))

        # Rectangular buttons
        button_width = 0.1
        button_height = 0.1
        button_x_offset = 1.55
        button_y_offset = -0.5
        button_spacing = 0.1

        self.segments.extend(
            SegmentPoly(
                [
                    (
                        button_x_offset,
                        button_y_offset + i * (button_height + button_spacing),
                    ),
                    (
                        button_x_offset + button_width,
                        button_y_offset + i * (button_height + button_spacing),
                    ),
                    (
                        button_x_offset + button_width,
                        button_y_offset
                        + i * (button_height + button_spacing)
                        + button_height,
                    ),
                    (
                        button_x_offset,
                        button_y_offset
                        + i * (button_height + button_spacing)
                        + button_height,
                    ),
                ],
                fill=False,
            )
            for i in range(3)
        )

        # Waveform on the screen
        def _make_noisy_sine(
            length: int = 120,
        ) -> Sequence[Tuple[float, float]]:
            path = []
            for x in range(length):
                y = 0.5 * disp_height * math.sin(
                    2 * math.pi * x / length
                ) + 0.3 * disp_height * (random.random() - 0.5)
                path.append((x / length * 0.8 * disp_width, 0.55 * y))
            return path

        path = _make_noisy_sine()
        path = [
            (x + disp_x_offset + 0.1 * disp_width, y + disp_y_offset + disp_height / 2)
            for x, y in path
        ]
        self.segments.append(Segment(path))


class OPM(Rectangle):
    def __init__(self, width=1.5, height=1, **kwargs):
        super().__init__(width=width, height=height, **kwargs)

        # Arc
        self.segments.append(
            SegmentArc((self.width / 2, -self.height / 5), 1, 1, theta1=20, theta2=160)
        )

        # Arrow
        self.segments.append(
            Segment(
                [(self.width / 2, -self.height / 5), (1, 0.17)],
                arrow="->",
                arrowlength=0.15,
                arrowwidth=0.1,
            )
        )

        # Fill circle at the beginning of the arrow
        self.segments.append(
            SegmentCircle((self.width / 2, -self.height / 5), 0.05, fill=True)
        )


class PD(Rectangle):
    def __init__(self, width=1, height=1, **kwargs):
        super().__init__(width=width, height=height, **kwargs)

        self.segments.append(
            Segment(
                [
                    (self.width / 2, -self.height / 2 + 0.1),
                    (self.width / 2, -self.height / 2 + 0.25),
                ]
            )
        )
        self.segments.append(
            SegmentPoly(
                [
                    (self.width / 4, -self.height / 2 + 0.25),
                    (self.width / 2, self.height / 2 - 0.45),
                    (3 * self.width / 4, -self.height / 2 + 0.25),
                ],
                fill=True,
            )
        )
        self.segments.append(
            Segment(
                [
                    (self.width / 4, self.height / 2 - 0.45),
                    (3 * self.width / 4, self.height / 2 - 0.45),
                ]
            )
        )
        self.segments.append(
            Segment(
                [
                    (self.width / 2, self.height / 2 - 0.45),
                    (self.width / 2, self.height / 2 - 0.25),
                ]
            )
        )

        x_ofst = 0.25
        y_ofst = 0.2

        self.segments.append(
            Segment(
                [
                    (0.0 + x_ofst, self.height / 6 + y_ofst),
                    (self.height / 6 + x_ofst, 0.0 + y_ofst),
                ],
                arrow="->",
                arrowlength=0.1,
                arrowwidth=0.06,
            )
        )

        x_ofst = 0.17
        y_ofst = 0.13

        self.segments.append(
            Segment(
                [
                    (0.0 + x_ofst, self.height / 6 + y_ofst),
                    (self.height / 6 + x_ofst, 0.0 + y_ofst),
                ],
                arrow="->",
                arrowlength=0.1,
                arrowwidth=0.06,
            )
        )


class LD(Rectangle):
    def __init__(self, width=1, height=1, **kwargs):
        super().__init__(width=width, height=height, **kwargs)

        self.segments.append(
            Segment(
                [
                    (self.width / 2, -self.height / 2 + 0.1),
                    (self.width / 2, -self.height / 2 + 0.25),
                ]
            )
        )
        self.segments.append(
            SegmentPoly(
                [
                    (self.width / 4, -self.height / 2 + 0.25),
                    (self.width / 2, self.height / 2 - 0.45),
                    (3 * self.width / 4, -self.height / 2 + 0.25),
                ],
                fill=True,
            )
        )
        self.segments.append(
            Segment(
                [
                    (self.width / 4, self.height / 2 - 0.45),
                    (3 * self.width / 4, self.height / 2 - 0.45),
                ]
            )
        )
        self.segments.append(
            Segment(
                [
                    (self.width / 2, self.height / 2 - 0.45),
                    (self.width / 2, self.height / 2 - 0.25),
                ]
            )
        )

        x_ofst = 0.62
        y_ofst = 0.22

        self.segments.append(
            Segment(
                [
                    (0.0 + x_ofst, 0.0 + y_ofst),
                    (self.height / 6 + x_ofst, self.height / 6 + y_ofst),
                ],
                arrow="->",
                arrowlength=0.1,
                arrowwidth=0.06,
            )
        )

        x_ofst = 0.7
        y_ofst = 0.15

        self.segments.append(
            Segment(
                [
                    (0.0 + x_ofst, 0.0 + y_ofst),
                    (self.height / 6 + x_ofst, self.height / 6 + y_ofst),
                ],
                arrow="->",
                arrowlength=0.1,
                arrowwidth=0.06,
            )
        )
