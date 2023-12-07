# Quick Docs

Assume we have a `C++` file like 

```
#include <iostream>

int func_1(int x , int y){
    
    std::cout << "Hello World! 1";
    
    return x;
}
```
|CMD|Jupyter|
|---|---|
|`pip install git+https://github.com/AyushSinghal9020/va_dev.git`|`! pip install git+https://github.com/AyushSinghal9020/va_dev.git`

To use the function 
```
from va_dev import va_dev as vdev

obj = vdev('c++')

lib = obj.load_lib('absolute path to the C++ file')

file = obj.load_func('func_1' , args = [0 , 1])

print(file)
```
```
0
```

# Working Overview
<img src = 'https://raw.githubusercontent.com/AyushSinghal9020/va_dev/main/vdev.drawio.png'>
