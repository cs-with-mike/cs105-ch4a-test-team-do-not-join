# Lexer & Parser for the Tokki Language
Westmont College CS 105 Fall 2023
Chapter 4 Assignment A

## Author Information
- **Mike Ryu** mryu@westmont.edu

## Overview
To practice the concepts we are learning throughout Chapter 4, we're going to be implementing a Syntax Analyzer. 
The first part of this is performing lexical analysis, or, in other words, implementing our own lexer.

## Design Notes
I made a Tokki class that has a default constructor that takes in a sentence and has as its attributes 
persistent variables to keep track of `lexeme`s, `next_char`, etc. `get_char` and `add_char` functions were
added to this class as methods since they mutate those persistent varaibles.

## Lessons Learned
Writing a lexer is fun!