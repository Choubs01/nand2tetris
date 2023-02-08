// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

(LOOP)
    @SCREEN
    D=A
    @addr
    M=D     //Stores and resets base screen address

    @KBD
    D=M
    @WHITE
    D; JEQ //Turn screen white if no button is pressed else @BLACK

    (BLACK)
        @addr 
        A=M
        M=-1 //Weird thing from video

        @addr
        MD=M+1 //Increment memory address by 1 each time and store it to D

        @KBD 
        D=A-D //Distance between current memory address and keyboard address (kbd address is upper limit of screen addresses)
        @LOOP
        D; JEQ 
        @BLACK
        0; JMP

    (WHITE)     //Same as @BLACK
        @addr
        A=M
        M=0

        @addr
        MD=M+1

        @KBD 
        D=A-D
        @LOOP
        D; JEQ 
        @WHITE
        0; JMP