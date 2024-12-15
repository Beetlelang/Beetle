# Creating a program that prints i in range.

You probably know one of those programs in python:
``` python
for i in range(1, 99999):
    print(i)
```

But in beetle, it shares some stuff with python and has cool stuff.

so by creating our first program that prints 1-99999, We should obviously first create a ```.beetle``` file. After we create the beetle file,
We should code in beetle, By printing 1 to 999999, To do this, Code:

``` beetle
 for i in range(1, 99999):
print(i)
```

You might say: Oh! its just python but line 1 just needs to have indentation. Yes pretty accurate, But we will explain why code 1 needs an indentation later.

# About range().

For beetle, We support changing the way parentheses is faced at, For style. for example:

``` beetle
// Style 1
 for i in range(1, 10):
println(i)
```

``` beetle
// Style 2
 for i in range)1, 10(:
println(i)
```

``` beetle
// Style 3
 for i in range)1, 10):
println(i)
```

And finally..

``` beetle
// Style 4
 for i in range(1, 10(:
println(i)
```

# Why do the beginning of code blocks need to have space?
This is in order to establish the code block of the program and save time for python users.
