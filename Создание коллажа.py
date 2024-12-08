import os
from PIL import Image, ImageDraw, ImageFont
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QFileDialog, QInputDialog

class CollageApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Collage Generator')

        layout = QtWidgets.QVBoxLayout()

        self.dirButton = QtWidgets.QPushButton('Выбрать папку с изображениями')
        self.dirButton.clicked.connect(self.select_directory)
        layout.addWidget(self.dirButton)

        self.titleButton = QtWidgets.QPushButton('Ввести заголовок')
        self.titleButton.clicked.connect(self.set_title)
        layout.addWidget(self.titleButton)

        self.gridButton = QtWidgets.QPushButton('Задать размер сетки (например, 2x3)')
        self.gridButton.clicked.connect(self.set_grid)
        layout.addWidget(self.gridButton)

        self.filterButton = QtWidgets.QPushButton('Применить чернобелый фильтр? (да/нет)')
        self.filterButton.clicked.connect(self.apply_filter)
        layout.addWidget(self.filterButton)

        self.sizeButton = QtWidgets.QPushButton('Задать размер коллажа (например, 800x600)')
        self.sizeButton.clicked.connect(self.set_collage_size)
        layout.addWidget(self.sizeButton)

        self.formatButton = QtWidgets.QPushButton('Выбрать формат выходного файла (jpg, png и т.д.)')
        self.formatButton.clicked.connect(self.set_format)
        layout.addWidget(self.formatButton)

        self.createButton = QtWidgets.QPushButton('Создать коллаж')
        self.createButton.clicked.connect(self.create_collage)
        layout.addWidget(self.createButton)

        self.setLayout(layout)

        self.directory = ""
        self.title = ""
        self.grid_size = (2, 2)
        self.filter = False
        self.collage_size = (800, 600)
        self.file_format = "png"

    def select_directory(self):
        self.directory = QFileDialog.getExistingDirectory(self, "Выбрать папку с изображениями")

    def set_title(self):
        self.title, ok = QInputDialog.getText(self, 'Ввод заголовка', 'Введите заголовок:')
        if not ok:
            self.title = ""

    def set_grid(self):
        grid_input, ok = QInputDialog.getText(self, 'Задать размер сетки', 'Введите размер сетки (ч/р):')
        if ok:
            try:
                rows, cols = map(int, grid_input.split('x'))
                self.grid_size = (rows, cols)
            except ValueError:
                pass

    def apply_filter(self):
        text, ok = QInputDialog.getText(self, 'Фильтр', 'Применить чернобелый фильтр? (да/нет)')
        if ok and text.lower() in ['да', 'yes']:
            self.filter = True
        else:
            self.filter = False

    def set_collage_size(self):
        size_input, ok = QInputDialog.getText(self, 'Задать размер коллажа', 'Введите размеры (ширина x высота):')
        if ok:
            try:
                width, height = map(int, size_input.split('x'))
                self.collage_size = (width, height)
            except ValueError:
                pass

    def set_format(self):
        self.file_format, ok = QInputDialog.getText(self, 'Формат файла', 'Введите формат файла (например, jpeg или png):')

    def create_collage(self):
        if not self.directory:
            print("Выберите папку с изображениями.")
            return

        images = [Image.open(os.path.join(self.directory, file)) for file in os.listdir(self.directory) if file.lower().endswith(('jpg', 'jpeg', 'png'))]

        if self.filter:
            images = [img.convert('L') for img in images]

        # Спецификация размера коллажа
        collage = Image.new('RGB', self.collage_size, (255, 255, 255))
        draw = ImageDraw.Draw(collage)
        width_cell = self.collage_size[0] // self.grid_size[1]
        height_cell = (self.collage_size[1] - 50) // self.grid_size[0]  # Оставляем место для заголовка

        # Добавление заголовка
        if self.title:
            try:
                font = ImageFont.truetype("arial.ttf", size = 30)  # Используем шрифт Arial с заданным размером
                draw.text((10, 10), self.title, font=font, fill='black')
            except Exception as e:
                print(f"Ошибка при добавлении текста: {e}")

        for index, image in enumerate(images):
            if index >= self.grid_size[0] * self.grid_size[1]:
                break
            image = image.resize((width_cell - 10, height_cell - 10))
            x = (index % self.grid_size[1]) * width_cell + 5
            y = (index // self.grid_size[1]) * height_cell + 50 + 5  # Смещаем вниз, чтобы оставить место для заголовка
            collage.paste(image, (x, y))

            # Рисуем рамку
            draw.rectangle([x, y, x + width_cell, y + height_cell + 50], outline="black", width=2)

        # Сохраняем коллаж в указанном формате
        try:
            collage.save(f"collage.{self.file_format.lower()}", format=self.file_format.upper())
            print("Коллаж создан!")
        except ValueError as e:
            print(f"Ошибка при сохранении файла: {e}")



if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = CollageApp()
    window.show()
    sys.exit(app.exec_())