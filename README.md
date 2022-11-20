# TaichiMusician
 团队名：范特西
 项目名：TaichiMusician
 项目介绍：灵感来源于世界上著名的音乐制作软件FL studio， Cubase及Logic Pro等，想借助于Taichi编程语言的的简洁性，高效性，编写一款操作简单的小型音乐制作软件，能够让使用者省去繁杂的乐理学习，用最简单的软件操作，快速制作一首流行歌曲伴奏，让普通人也能快速进入创造音乐的Fantasy世界。
 本项目的制作，涉及不同音色乐器的音频处理，音符播放的时间顺序逻辑，不同音调音符的拆解。对于具体的不同音色，短促型打击乐器及弦乐类乐器的播放逻辑有所区别，需进行不同的声音时值处理。
 本项目可拆解为几个步骤：
 1. 界面设计：设计为琴键加网格的布局，琴键不同八度区域对应不同音色乐器的不同音调，网格部分按照小节和拍子划分区域，以满足音乐节奏及声音时值的量化。
 2. 播放逻辑：整体不断循环播放，依照BPM控制时间条的前进速度，使其按照拍子正确运行到所制作音乐的正确播放位置，前进到对应位置播放对应位置的音符从而组合出整体的音乐效果。
 3. 乐器设计：为了简化问题，仅采用钢琴、贝斯、鼓及弦乐类乐器，这种乐器组合已经可以满足大部分音乐的制作。对于具体的乐器例如钢琴，对1或2个八度音内的钢琴音色进行采样，提取成wav文件。第三方库pygame的mixer模块可以读取wav文件并播放其声音内容，因此可以通过编写代码实现将声音映射到软件内不同音色音调对应的网格区域，从而使得软件播放到对应位置时发出对应乐器的对应音高的声音。
 其他：本项目仅采用Tachi编程语言及第三方库Pygame。
