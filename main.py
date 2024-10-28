from generate import Generator


def main():
    size_x = 4000
    size_y = 4000
    generator = Generator(size_x, size_y)
    generator.generate()
    generator.print_maze("maze.png")
    generator.go_maze()
    generator.print_maze("maze_go.png")


if __name__ == '__main__':
    main()
