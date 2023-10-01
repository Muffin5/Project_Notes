from PIL import Image, ImageDraw


class Tab:
    def __init__(self, fret, string, dist):  # dist ставим 0 в списке диапозона
        self.fret = fret
        self.string = string
        self.dist = dist


ukulele_range_pitch = [
    "C4",
    "D4",
    "E4",
    "F4",
    "G4",
    "A4",
    "H4",
    "C5",
    "D5",
    "E5",
    "F5",
    "G5",
    "A5",
]
ukulele_range_tabs = [
    Tab(0, 3, 0),
    Tab(2, 3, 0),
    Tab(0, 2, 0),
    Tab(1, 2, 0),
    Tab(0, 4, 0),
    Tab(0, 1, 0),
    Tab(2, 1, 0),
    Tab(3, 1, 0),
    Tab(5, 1, 0),
    Tab(7, 1, 0),
    Tab(8, 1, 0),
    Tab(10, 1, 0),
    Tab(12, 1, 0),
]


def convert_one(note):
    if note.clef == "violin" and note.pitch in ukulele_range_pitch:
        answer = ukulele_range_tabs[ukulele_range_pitch.index(note.pitch)]
    else:
        answer = Tab(-1, -1, -1)
    return answer


def convert(notes):
    answer = []
    for i in range(0, len(notes)):
        if i != (len(notes) - 1):
            tab = convert_one(notes[i])
            if tab.fret == -1:
                return []
            x, y = notes[i + 1].center
            x2, y2 = notes[i].center
            distance = x - x2
            tab.dist = distance
            answer.append(tab)
        else:
            tab = convert_one(notes[i])
            if tab.fret == -1:
                return []
            tab.dist = -1
            answer.append(tab)
    return answer


def draw_tabs(img, mass):
    draw = ImageDraw.Draw(img)
    draw.line((10, 30, 490, 30), fill="black", width=1)
    draw.line((10, 37, 490, 37), fill="black", width=1)
    draw.line((10, 44, 490, 44), fill="black", width=1)
    draw.line((10, 51, 490, 51), fill="black", width=1)
    print(mass[0].fret, mass[0].string)

    line_heights = [30, 37, 44, 51]
    buffer = 10

    print(len(mass))
    for i in range(0, len(mass)):
        if mass[i].dist != -1:
            buffer+=int(abs(mass[i].dist))/10
            if buffer > 490:
                buffer = 10
                line_heights[0]+=36
                line_heights[1]+=36
                line_heights[2]+=36
                line_heights[3]+=36
                draw.line((10, line_heights[0], 490, line_heights[0]), fill="black", width=1)
                draw.line((10, line_heights[1], 490, line_heights[1]), fill="black", width=1)
                draw.line((10, line_heights[2], 490, line_heights[2]), fill="black", width=1)
                draw.line((10, line_heights[3], 490, line_heights[3]), fill="black", width=1)
            draw.text((buffer, line_heights[mass[i].string-1] - 5), str(mass[i].fret), fill="black")

    # draw.text((10,25), str(mass[0].fret), fill = "black")

    return img
