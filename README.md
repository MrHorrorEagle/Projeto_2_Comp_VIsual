# Projeto 2
Repositório destinado ao Projeto 2 da disciplina de Computação Visual

Prof° André Kishimoto
```
Fabio Oliveira da Silva - 10420458
Patrick Rocha de Andrade - 10410902
```
A opção escolhida para a realização desse projeto foi a 4, aplicação prática (software). O projeto consiste em um software de detector de bordas de uma imagem, que pode ser escolhida em um menu interativo, gerando algumas imagens usando filtro de Sobel, Laplace e um algoritmo de Canny. Além disso é possível gerar um gráfico em 3D que representa as bordas da imagem.

O Link para o vídeo se encontra aqui: [Link](Colocar aqui o Link)

O código em python usado para gerar o software encontra-se nesse repositório com o nome mapa_bordas.py, o executável .exe ficou muito pesado, o que impossibilitou o upload do mesmo no github. Em caso de execução local, as bibliotecas necessárias para tal se encontram no cabeçalho do código.

Instruções para rodar o código localmente:
	- Para rodar o código .py, é necessário que as seguintes bibliotecas estejam instaladas:
		- Opencv-python
		- matplotlib
		- numpy

Para instalar as mesmas basta rodar o comando:
		- pip install matplotlib

- Para compilar o código em um .exe, é necessário instalar a biblioteca pyinstaller
	- pip install pyinstaller
- Após instalar, rodar o comando:
	- pyinstaller --onefile --windowed --name MapaBordas --hidden-import matplotlib.backends.backend_tkagg --hidden-import mpl_toolkits.mplot3d mapa_bordas.py

Referências do projeto:
	- Materiais de aula, material de "Detecção de Bordas"
	- OpenCV – Canny Edge Detection: https://docs.opencv.org/4.x/da/d22/tutorial_py_canny.html
	- OpenCV – Sobel Derivatives: https://docs.opencv.org/4.x/d2/d2c/tutorial_sobel_derivatives.html
	- OpenCV – Laplace Operator: https://docs.opencv.org/4.x/d5/db5/tutorial_laplace_operator.html
	- Matplotlib – 3D surface: https://matplotlib.org/stable/gallery/mplot3d/surface3d.html
	- NumPy: https://numpy.org/doc/stable/
	- Tkinter: https://docs.python.org/3/library/tkinter.html
	- PyInstaller: https://pyinstaller.org/en/stable/
