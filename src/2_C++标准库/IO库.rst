.. contents::
   :depth: 3
..

IO库
====

最基本的 IO 库设施包括：

-  ``istream``\ ：输入流类型，提供输入操作。
-  ``ostream``\ ：输出流类型，提供输出操作。
-  ``cin``\ ：\ ``istream``\ 对象，从标准输入读取数据。
-  ``cout``\ ：\ ``ostream``\ 对象，向标准输出写入数据。
-  ``cerr``\ ：\ ``ostream``\ 对象，向标准错误写入数据。
-  ``>>``\ 运算符：从\ ``istream``\ 对象读取输入数据。
-  ``<<``\ 运算符：向\ ``ostream``\ 对象写入输出数据。
-  ``getline``\ 函数：从\ ``istream``\ 对象读取一行数据，写入\ ``string``\ 对象。

IO类
----

``iostream`` 定义基础类型，\ ``fstream``
定义针对文件的输入输出，\ ``sstream`` 定义针对 ``string``
的输入输出。如：

-  ``iostream`` 头文件：\ ``istream``\ 、\ ``wistream``
   从流中读取，\ ``ostream``\ 、\ ``wostream``
   写入流，\ ``iostream``\ 、\ ``wiostream`` 对流进行读写。
-  ``fstream`` 头文件：\ ``ifstream``\ 、\ ``wifstream``
   从文件中读取，\ ``ofstream``\ 、\ ``wofstream``
   写文件，\ ``fstream``\ 、\ ``wfstream`` 对文件进行读写。
-  ``sstream`` 头文件：\ ``istringstream``\ 、\ ``wistringstream``
   从字符串中读取，\ ``ostringstream``\ 、\ ``wostringstream``
   写入到字符串中，\ ``stringstream``\ 、\ ``wstringstream``
   对字符串进行读写。

为了支持宽字符集，标准库定义了处理 ``wchat_t``
数据的类型和对象。宽字符版本通常以 ``w`` 开头，如
``wcin``\ ，\ ``wcout``\ ，\ ``wcerr`` 是
``cin``\ ，\ ``cout``\ ，\ ``cerr`` 的款字符对应对象。

不能拷贝或赋值 IO 对象
~~~~~~~~~~~~~~~~~~~~~~

IO 类型的对象是不可以拷贝或赋值的，函数只能传递或者返回流对象的引用。

读取或写入 IO 对象会改变起状态，所以引用必须不是 ``const`` 的。

条件状态
~~~~~~~~

IO
操作不可避免地会出现错误，有些错误是可以恢复的，如格式错误；有些错误则深入到系统中，并且超出了程序可以修正的范围。

检查流的状态
^^^^^^^^^^^^

IO 对象使用一个机器相关的整形 ``iostate`` 来承载状态信息。这个类型是一个
``bit`` 的集合。IO 类同时定义了 4 个常量值来表示不同的 ``bit``
模式，它们用于表示不同的 IO 状态。这些值可以通过位操作符来测试和设置。7

-  ``strm::iostate``\ ：\ ``strm`` 是一个 IO 类型，\ ``iostate``
   是一个机器相关的整形类型用于表示 ``stream`` 的条件状态。
-  ``strm::badbit``\ ：常量值，可以赋值给
   ``strm::iostate``\ ，用于表示流被损坏了。
-  ``strm::failbit``\ ：常量值，可以赋值给 ``strm::iostate`` 用于表示 IO
   操作失败了。
-  ``strm::eofbit``\ ：常量值，可以赋值给 ``strm::iostate``
   用于表示流到了 ``end-of-file``\ 。
-  ``strm::goodbit``\ ：常量值，可以赋值给
   ``strm::iostate``\ ，用于表示流没有遇到错误，这个值保证是 0。

-  ``s.eof()``\ ：当流对象的 ``eofbit`` 被设置时返回 ``true``\ 。
-  ``s.fail()``\ ：如果流对象的 ``failbit`` 或 ``badbit`` 被设置时返回
   ``true``\ 。
-  ``s.bad()``\ ：如果流对象的 ``badbit`` 被设置时返回 ``true``\ 。
-  ``s.good()``\ ：如果流对象状态没有任何错误时返回 ``true``\ 。

注意：

-  ``badbit`` 表示系统级错误，如不可恢复的读写错误。通常情况下，一旦
   ``badbit`` 被置位，流就无法继续使用了。
-  在发生可恢复错误后，\ ``failbit``
   会被置位，如期望读取数值却读出一个字符。
-  如果到达文件结束位置， ``eofbit`` 和 ``failbit`` 都会被置位。
-  如果流未发生错误，则 ``goodbit`` 的值为0。
-  如果 ``badbit``\ 、\ ``failbit`` 和 ``eofbit``
   任何一个被置位，检测流状态的条件都会失败。
-  ``good`` 函数在所有错误均未置位时返回 ``true``\ 。
-  ``bad``\ 、\ ``fail``\ 和 ``eof`` 函数在对应错误位被置位时返回
   ``true``\ 。
-  在 ``badbit`` 被置位时，\ ``fail`` 函数也会返回
   ``true``\ 。因此应该使用 ``good`` 或 ``fail``
   函数确定流的总体状态，\ ``eof`` 和 ``bad`` 只能检测特定错误。

管理条件状态
^^^^^^^^^^^^

-  ``s.clear()``\ ：将流对象状态设置为没有错误，返回 ``void``\ 。
-  ``s.clear(flags)``\ ：将流对象的状态设置为 ``flags`` 所表示的值，它是
   ``strm::iostate`` 类型。
-  ``s.setstate(flags)``\ ：在 ``s`` 上添加特定的条件状态
   ``flags``\ ，\ ``flags`` 的类型时\ ``strm::iostate``\ ，返回
   ``void``\ 。
-  ``s.rdstate()``\ ：返回 ``s`` 的当前条件状态，返回类型是
   ``strm::iostate``\ 。

管理输出缓冲
~~~~~~~~~~~~

每个输出流都管理一个缓冲区，用于保存程序读写的数据。导致缓冲刷新（即数据真正写入输出设备或文件）的原因有很多：

-  程序正常结束。
-  缓冲区已满。
-  使用操纵符（如：\ ``endl``\ ）显式刷新缓冲区。
-  在每个输出操作之后，可以用 ``unitbuf``
   操纵符设置流的内部状态，从而清空缓冲区。默认情况下，对 ``cerr``
   是设置 ``unitbuf`` 的，因此写到 ``cerr`` 的内容都是立即刷新的。
-  一个输出流可以被关联到另一个流。这种情况下，当读写被关联的流时，关联到的流的缓冲区会被刷新。默认情况下，\ ``cin``
   和 ``cerr`` 都关联到 ``cout``\ ，因此，读 ``cin`` 或写 ``cerr``
   都会刷新 ``cout`` 的缓冲区。

刷新缓冲区，可以使用如下IO操纵符：

-  ``endl``\ ：输出一个换行符并刷新缓冲区。
-  ``flush``\ ：刷新流，单不添加任何字符。
-  ``ends``\ ：在缓冲区插入空字符\ ``null``\ ，然后刷新。
-  ``unitbuf``\ ：告诉流接下来每次操作之后都要进行一次\ ``flush``\ 操作。
-  ``nounitbuf``\ ：回到正常的缓冲方式:

::

   cout << unitbuf; 
   cout << nounitbuf;

当程序意外终止时输出缓冲是不会刷新的，此时程序写入的数据很可能还在缓冲中等待被打印。当你调试一个崩溃的程序时，确保你认为应该输出的数据确实刷新了。

将输入流和输出流绑在一起
^^^^^^^^^^^^^^^^^^^^^^^^

交互式系统应该将其输入流绑定到输出流上，这样做意味着所有的读操作之前都会将缓冲中的数据刷新出去。

``tie`` 函数有两个版本：

-  没有参数，如果它绑定了一个输出流，返回一个输出流的指针，否则返回
   ``nullptr``\ 。
-  接受一个 ``ostream``
   类型的指针，并将其绑定到这个流上。如：\ ``x.tie(&o)`` 将流 x
   绑定到输出流 o 上，这样 x 的任何操作将导致 o 的输出缓冲被刷新。

::

   cin.tie(&cout);  //@ 仅仅展示:标准库 cin 和 cout 关联在一起
   //@ old_tie 指向当前关联到的 cin 的流
   ostream *old_tie = cin.tie(nullptr); //@ cin 不再与其他流关联
   cin.tie(&cerr); //@ cin 将与 cerr 关联，读取 cin 会刷新 cerr 而不是cout 
   cin.tie(old_tie); //@ 重建 cin 和 cout 之间的关联

文件输入输出
------------

头文件 ``<fstream>`` 定义了三个支持文件 IO 的类型：

-  ``ifstream``\ 从一个给定文件读取数据。
-  ``ofstream``\ 向一个给定文件写入数据。
-  ``fstream``\ 可以读写给定文件。

文件流：需要读写文件时，必须定义自己的文件流对象，并绑定在需要的文件上。

``fstream`` 特有的操作：

-  ``fstream fstrm;`` ：创建一个没有关联文件的文件流，\ ``fstream``
   是定义在 ``fstream`` 头文件中的一个类型。
-  ``fstream fstrm(s);`` ：创建一个 ``fstream`` 并打开名为 ``s``
   的文件，\ ``s`` 可以是 ``string`` 类型或者是一个 C
   风格字符串指针，这个构造函数是 ``explicit``
   的，默认的文件模式取决于\ ``fstream`` 的类型。
-  ``fstream fstrm(s, mode);`` ：与上一个构造函数类似，但是以给定的模式
   ``mode`` 打开 ``s`` 文件。
-  ``fstrm.open(s)`` ：打开名为 ``s`` 的文件，将其关联到 ``fstrm``
   对象上，\ ``s`` 可以是 ``string`` 或者 C
   风格字符串指针，默认的文件模式取决于 ``fstrm`` 的类型，返回
   ``void``\ 。
-  ``fstrm.close()`` ：关闭与\ ``fstrm`` 关联的文件，返回\ ``void``\ 。
-  ``fstrm.is_open()`` ：返回一个 ``bool`` 值告知是否此 ``fstrm``
   关联的文件已经成功打开，并且没有被关闭。

使用文件流对象
~~~~~~~~~~~~~~

当创建文件流对象时可以选择性的提供一个文件名，如果提供了文件名，那么
``open`` 就会自动调用。如：

::

   ifstream in(ifile); 

当定义一个空的文件流对象时，可以接着在后面通过 ``open``
将其关联到一个文件上。如：

::

   ofstream out;
   out.open(ifile + ".copy"); 

当调用 ``open`` 失败时，会设置 ``failbit``\ ，由于 ``open``
可能会失败，所以最好需要验证一下 ``open`` 是否成功。如：

::

   if (out)   //@ 检查是否被open

如果打开失败，条件将会失败，我们就不能使用 ``out`` 对象。

一旦一个文件流对象被打开，它将与给定的文件持续关联。如果在一个已经打开的文件流对象上调用
``open`` 将会失败，并且设置
``failbit``\ 。接下来尝试使用这个文件流将会失败。为了将文件流对象关联到一个不同的文件上，需要选将之前的文件关闭，才能打开新的文件。如：

::

   in.close();
   in.open(ifile + "2");

自动构建和析构：

::

   for (auto p = argv + 1; p != argv + argc; ++p) {
       ifstream input(*p);
       if (input) {
           process(input);
       } else
           cerr << "couldn't open: " + string(*p);
   }

每次迭代时都会自动创建一个新的 ``ifstream`` 对象并打开给定文件。由于
``input`` 是 ``while``
中的本地对象，它将在每次迭代时自动的创建和销毁。当 ``fstream``
对象离开作用域之后，与其关联的文件会自动关闭。在下一次迭代时会创建一个新的。

文件模式
~~~~~~~~

每个流都有与之关联的文件模式来代表文件可以如何被使用。以下列举文件模式和它们的含义：

========== ============================
文件模式   解释
========== ============================
``in``     以读的方式打开
``out``    以写的方式打开
``app``    每次写操作前均定位到文件末尾
``ate``    打开文件后立即定位到文件末尾
``trunc``  截断文件
``binary`` 以二进制方式进行IO操作。
========== ============================

可以指定的文件模式有一些限制：

-  只能对 ``ofstream`` 或 ``fstream`` 对象设定 ``out`` 模式。
-  只能对 ``ifstream`` 或 ``fstream`` 对象设定 ``in`` 模式。
-  只有当 ``out`` 被设定时才能设定 ``trunc`` 模式。
-  只要 ``trunc`` 没有被设定，就能设定 ``app`` 模式。在 ``app``
   模式下，即使没有设定 ``out`` 模式，文件也是以输出方式打开。
-  默认情况下，即使没有设定 ``trunc``\ ，以 ``out``
   模式打开的文件也会被截断。如果想保留以 ``out``
   模式打开的文件内容，就必须同时设定 ``app``
   模式，这会将数据追加写到文件末尾；或者同时设定 ``in``
   模式，即同时进行读写操作。
-  ``ate`` 和 ``binary``
   模式可用于任何类型的文件流对象，并可以和其他任何模式组合使用。
-  与 ``ifstream`` 对象关联的文件默认以 ``in`` 模式打开，与 ``ofstream``
   对象关联的文件默认以 ``out`` 模式打开，与 ``fstream``
   对象关联的文件默认以 ``in`` 和 ``out`` 模式打开。

string流
--------

头文件 ``sstream``\ ：

-  ``istringstream`` 从 ``string`` 读取数据。
-  ``ostringstream`` 向 ``string`` 写入数据。
-  ``stringstream`` 可以读写给定 ``string``\ 。

``stringstream`` 特有的操作，\ ``sstream`` 是头文件 ``sstream``
中任意一个类型，\ ``s`` 是一个 ``string``\ ：

-  ``sstream strm``\ ：定义一个未绑定的 ``stringstream`` 对象。
-  ``sstream strm(s)``\ ：用 ``s`` 初始化对象。
-  ``strm.str()``\ ：返回 ``strm`` 所保存的 ``string`` 的拷贝。
-  ``strm.str(s)``\ ：将 ``s`` 拷贝到 ``strm`` 中，返回 ``void``\ 。

使用istringstream
~~~~~~~~~~~~~~~~~

::

   struct PersonInfo
   {
       string name;
       vector<string> phones;
   };

   string line, word; 
   vector<PersonInfo> people;   

   while (getline(cin, line))
   {
       PersonInfo info;    
       istringstream record(line);    
       record >> info.name;    
       while (record >> word)  
           info.phones.push_back(word);  
       people.push_back(info);  
   }

使用ostringstream
~~~~~~~~~~~~~~~~~

::

   for (const auto &entry : people)
   { 
       ostringstream formatted, badNums;   
       for (const auto &nums : entry.phones)
       { 
           if (!valid(nums))
           {
               badNums << " " << nums;  
           }
           else
               formatted << " " << format(nums);
       }

       if (badNums.str().empty())  
           os << entry.name << " "
               << formatted.str() << endl;  
       else  
           cerr << "input error: " << entry.name
               << " invalid number(s) " << badNums.str() << endl;
   }
