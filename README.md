# Prim

A Python implementation on Kruskal's minimum spanning tree algorithm

## Getting Started

Download, clone or copy the code from the repository into a .py file

```
""" Example on how to setup and run the Kruskal's algorithm """

    # Initiates an instance of Kruskal's class
    k = Kruskal()
    
    # Add vertexes with any custom Label
    k.graph.add_vertexes(['A', 'B', 'C', 'D', 'E'])
    
    # Adds connections between the vertexes. Labels must match with already added vertexes
    k.graph.add_connections([
        ('A', 3, 'B'),
        ('A', 1, 'E'),
        ('B', 5, 'C'),
        ('B', 4, 'E'),
        ('C', 6, 'E'),
        ('C', 2, 'D'),
        ('D', 7, 'E')
    ])

    # Solves and returns a SpanningTree object, with all the information stored inside it
    minimum_spanning_tree = k.solve()
    print(minimum_spanning_tree)
    
```

### Prerequisites

Python 3

## Running the tests

You can simply run the file to see the given output. The example is by the end of the file, and it starts on the function

```
if __name__ == '__main__':
```

## Contributing

Any contribution is very welcome to the project (Code, suggestions and even errors/bug reports). If you do wish to help, please contact me at: lucasbbr98@gmail.com


## Authors

* **Lucas Arruda Bonservizzi** - *Initial work* - [lucasbbr98](https://github.com/lucasbbr98)


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Inspiration 1: I enjoyed an Operations Research class from professor Cleber Rocco at UNICAMP - FCA.
* Inspiration 2: Maybe my code can help someone around the world. 
* Feel free to contact me if you need any help at lucasbbr98@gmail.com.
