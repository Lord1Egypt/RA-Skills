#!/usr/bin/env node
"use strict";
var __create = Object.create;
var __defProp = Object.defineProperty;
var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
var __getOwnPropNames = Object.getOwnPropertyNames;
var __getProtoOf = Object.getPrototypeOf;
var __hasOwnProp = Object.prototype.hasOwnProperty;
var __commonJS = (cb, mod) => function __require() {
  return mod || (0, cb[__getOwnPropNames(cb)[0]])((mod = { exports: {} }).exports, mod), mod.exports;
};
var __copyProps = (to, from, except, desc) => {
  if (from && typeof from === "object" || typeof from === "function") {
    for (let key of __getOwnPropNames(from))
      if (!__hasOwnProp.call(to, key) && key !== except)
        __defProp(to, key, { get: () => from[key], enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable });
  }
  return to;
};
var __toESM = (mod, isNodeMode, target) => (target = mod != null ? __create(__getProtoOf(mod)) : {}, __copyProps(
  // If the importer is in node compatibility mode or this is not an ESM
  // file that has been converted to a CommonJS file using a Babel-
  // compatible transform (i.e. "__esModule" has not been set), then set
  // "default" to the CommonJS "module.exports" for node compatibility.
  isNodeMode || !mod || !mod.__esModule ? __defProp(target, "default", { value: mod, enumerable: true }) : target,
  mod
));

// ../../node_modules/.pnpm/commander@13.1.0/node_modules/commander/lib/error.js
var require_error = __commonJS({
  "../../node_modules/.pnpm/commander@13.1.0/node_modules/commander/lib/error.js"(exports2) {
    "use strict";
    var CommanderError2 = class extends Error {
      /**
       * Constructs the CommanderError class
       * @param {number} exitCode suggested exit code which could be used with process.exit
       * @param {string} code an id string representing the error
       * @param {string} message human-readable description of the error
       */
      constructor(exitCode, code, message) {
        super(message);
        Error.captureStackTrace(this, this.constructor);
        this.name = this.constructor.name;
        this.code = code;
        this.exitCode = exitCode;
        this.nestedError = void 0;
      }
    };
    var InvalidArgumentError2 = class extends CommanderError2 {
      /**
       * Constructs the InvalidArgumentError class
       * @param {string} [message] explanation of why argument is invalid
       */
      constructor(message) {
        super(1, "commander.invalidArgument", message);
        Error.captureStackTrace(this, this.constructor);
        this.name = this.constructor.name;
      }
    };
    exports2.CommanderError = CommanderError2;
    exports2.InvalidArgumentError = InvalidArgumentError2;
  }
});

// ../../node_modules/.pnpm/commander@13.1.0/node_modules/commander/lib/argument.js
var require_argument = __commonJS({
  "../../node_modules/.pnpm/commander@13.1.0/node_modules/commander/lib/argument.js"(exports2) {
    "use strict";
    var { InvalidArgumentError: InvalidArgumentError2 } = require_error();
    var Argument2 = class {
      /**
       * Initialize a new command argument with the given name and description.
       * The default is that the argument is required, and you can explicitly
       * indicate this with <> around the name. Put [] around the name for an optional argument.
       *
       * @param {string} name
       * @param {string} [description]
       */
      constructor(name, description) {
        this.description = description || "";
        this.variadic = false;
        this.parseArg = void 0;
        this.defaultValue = void 0;
        this.defaultValueDescription = void 0;
        this.argChoices = void 0;
        switch (name[0]) {
          case "<":
            this.required = true;
            this._name = name.slice(1, -1);
            break;
          case "[":
            this.required = false;
            this._name = name.slice(1, -1);
            break;
          default:
            this.required = true;
            this._name = name;
            break;
        }
        if (this._name.length > 3 && this._name.slice(-3) === "...") {
          this.variadic = true;
          this._name = this._name.slice(0, -3);
        }
      }
      /**
       * Return argument name.
       *
       * @return {string}
       */
      name() {
        return this._name;
      }
      /**
       * @package
       */
      _concatValue(value, previous) {
        if (previous === this.defaultValue || !Array.isArray(previous)) {
          return [value];
        }
        return previous.concat(value);
      }
      /**
       * Set the default value, and optionally supply the description to be displayed in the help.
       *
       * @param {*} value
       * @param {string} [description]
       * @return {Argument}
       */
      default(value, description) {
        this.defaultValue = value;
        this.defaultValueDescription = description;
        return this;
      }
      /**
       * Set the custom handler for processing CLI command arguments into argument values.
       *
       * @param {Function} [fn]
       * @return {Argument}
       */
      argParser(fn) {
        this.parseArg = fn;
        return this;
      }
      /**
       * Only allow argument value to be one of choices.
       *
       * @param {string[]} values
       * @return {Argument}
       */
      choices(values) {
        this.argChoices = values.slice();
        this.parseArg = (arg, previous) => {
          if (!this.argChoices.includes(arg)) {
            throw new InvalidArgumentError2(
              `Allowed choices are ${this.argChoices.join(", ")}.`
            );
          }
          if (this.variadic) {
            return this._concatValue(arg, previous);
          }
          return arg;
        };
        return this;
      }
      /**
       * Make argument required.
       *
       * @returns {Argument}
       */
      argRequired() {
        this.required = true;
        return this;
      }
      /**
       * Make argument optional.
       *
       * @returns {Argument}
       */
      argOptional() {
        this.required = false;
        return this;
      }
    };
    function humanReadableArgName(arg) {
      const nameOutput = arg.name() + (arg.variadic === true ? "..." : "");
      return arg.required ? "<" + nameOutput + ">" : "[" + nameOutput + "]";
    }
    exports2.Argument = Argument2;
    exports2.humanReadableArgName = humanReadableArgName;
  }
});

// ../../node_modules/.pnpm/commander@13.1.0/node_modules/commander/lib/help.js
var require_help = __commonJS({
  "../../node_modules/.pnpm/commander@13.1.0/node_modules/commander/lib/help.js"(exports2) {
    "use strict";
    var { humanReadableArgName } = require_argument();
    var Help2 = class {
      constructor() {
        this.helpWidth = void 0;
        this.minWidthToWrap = 40;
        this.sortSubcommands = false;
        this.sortOptions = false;
        this.showGlobalOptions = false;
      }
      /**
       * prepareContext is called by Commander after applying overrides from `Command.configureHelp()`
       * and just before calling `formatHelp()`.
       *
       * Commander just uses the helpWidth and the rest is provided for optional use by more complex subclasses.
       *
       * @param {{ error?: boolean, helpWidth?: number, outputHasColors?: boolean }} contextOptions
       */
      prepareContext(contextOptions) {
        this.helpWidth = this.helpWidth ?? contextOptions.helpWidth ?? 80;
      }
      /**
       * Get an array of the visible subcommands. Includes a placeholder for the implicit help command, if there is one.
       *
       * @param {Command} cmd
       * @returns {Command[]}
       */
      visibleCommands(cmd) {
        const visibleCommands = cmd.commands.filter((cmd2) => !cmd2._hidden);
        const helpCommand = cmd._getHelpCommand();
        if (helpCommand && !helpCommand._hidden) {
          visibleCommands.push(helpCommand);
        }
        if (this.sortSubcommands) {
          visibleCommands.sort((a, b) => {
            return a.name().localeCompare(b.name());
          });
        }
        return visibleCommands;
      }
      /**
       * Compare options for sort.
       *
       * @param {Option} a
       * @param {Option} b
       * @returns {number}
       */
      compareOptions(a, b) {
        const getSortKey = (option) => {
          return option.short ? option.short.replace(/^-/, "") : option.long.replace(/^--/, "");
        };
        return getSortKey(a).localeCompare(getSortKey(b));
      }
      /**
       * Get an array of the visible options. Includes a placeholder for the implicit help option, if there is one.
       *
       * @param {Command} cmd
       * @returns {Option[]}
       */
      visibleOptions(cmd) {
        const visibleOptions = cmd.options.filter((option) => !option.hidden);
        const helpOption = cmd._getHelpOption();
        if (helpOption && !helpOption.hidden) {
          const removeShort = helpOption.short && cmd._findOption(helpOption.short);
          const removeLong = helpOption.long && cmd._findOption(helpOption.long);
          if (!removeShort && !removeLong) {
            visibleOptions.push(helpOption);
          } else if (helpOption.long && !removeLong) {
            visibleOptions.push(
              cmd.createOption(helpOption.long, helpOption.description)
            );
          } else if (helpOption.short && !removeShort) {
            visibleOptions.push(
              cmd.createOption(helpOption.short, helpOption.description)
            );
          }
        }
        if (this.sortOptions) {
          visibleOptions.sort(this.compareOptions);
        }
        return visibleOptions;
      }
      /**
       * Get an array of the visible global options. (Not including help.)
       *
       * @param {Command} cmd
       * @returns {Option[]}
       */
      visibleGlobalOptions(cmd) {
        if (!this.showGlobalOptions) return [];
        const globalOptions = [];
        for (let ancestorCmd = cmd.parent; ancestorCmd; ancestorCmd = ancestorCmd.parent) {
          const visibleOptions = ancestorCmd.options.filter(
            (option) => !option.hidden
          );
          globalOptions.push(...visibleOptions);
        }
        if (this.sortOptions) {
          globalOptions.sort(this.compareOptions);
        }
        return globalOptions;
      }
      /**
       * Get an array of the arguments if any have a description.
       *
       * @param {Command} cmd
       * @returns {Argument[]}
       */
      visibleArguments(cmd) {
        if (cmd._argsDescription) {
          cmd.registeredArguments.forEach((argument) => {
            argument.description = argument.description || cmd._argsDescription[argument.name()] || "";
          });
        }
        if (cmd.registeredArguments.find((argument) => argument.description)) {
          return cmd.registeredArguments;
        }
        return [];
      }
      /**
       * Get the command term to show in the list of subcommands.
       *
       * @param {Command} cmd
       * @returns {string}
       */
      subcommandTerm(cmd) {
        const args = cmd.registeredArguments.map((arg) => humanReadableArgName(arg)).join(" ");
        return cmd._name + (cmd._aliases[0] ? "|" + cmd._aliases[0] : "") + (cmd.options.length ? " [options]" : "") + // simplistic check for non-help option
        (args ? " " + args : "");
      }
      /**
       * Get the option term to show in the list of options.
       *
       * @param {Option} option
       * @returns {string}
       */
      optionTerm(option) {
        return option.flags;
      }
      /**
       * Get the argument term to show in the list of arguments.
       *
       * @param {Argument} argument
       * @returns {string}
       */
      argumentTerm(argument) {
        return argument.name();
      }
      /**
       * Get the longest command term length.
       *
       * @param {Command} cmd
       * @param {Help} helper
       * @returns {number}
       */
      longestSubcommandTermLength(cmd, helper) {
        return helper.visibleCommands(cmd).reduce((max, command) => {
          return Math.max(
            max,
            this.displayWidth(
              helper.styleSubcommandTerm(helper.subcommandTerm(command))
            )
          );
        }, 0);
      }
      /**
       * Get the longest option term length.
       *
       * @param {Command} cmd
       * @param {Help} helper
       * @returns {number}
       */
      longestOptionTermLength(cmd, helper) {
        return helper.visibleOptions(cmd).reduce((max, option) => {
          return Math.max(
            max,
            this.displayWidth(helper.styleOptionTerm(helper.optionTerm(option)))
          );
        }, 0);
      }
      /**
       * Get the longest global option term length.
       *
       * @param {Command} cmd
       * @param {Help} helper
       * @returns {number}
       */
      longestGlobalOptionTermLength(cmd, helper) {
        return helper.visibleGlobalOptions(cmd).reduce((max, option) => {
          return Math.max(
            max,
            this.displayWidth(helper.styleOptionTerm(helper.optionTerm(option)))
          );
        }, 0);
      }
      /**
       * Get the longest argument term length.
       *
       * @param {Command} cmd
       * @param {Help} helper
       * @returns {number}
       */
      longestArgumentTermLength(cmd, helper) {
        return helper.visibleArguments(cmd).reduce((max, argument) => {
          return Math.max(
            max,
            this.displayWidth(
              helper.styleArgumentTerm(helper.argumentTerm(argument))
            )
          );
        }, 0);
      }
      /**
       * Get the command usage to be displayed at the top of the built-in help.
       *
       * @param {Command} cmd
       * @returns {string}
       */
      commandUsage(cmd) {
        let cmdName = cmd._name;
        if (cmd._aliases[0]) {
          cmdName = cmdName + "|" + cmd._aliases[0];
        }
        let ancestorCmdNames = "";
        for (let ancestorCmd = cmd.parent; ancestorCmd; ancestorCmd = ancestorCmd.parent) {
          ancestorCmdNames = ancestorCmd.name() + " " + ancestorCmdNames;
        }
        return ancestorCmdNames + cmdName + " " + cmd.usage();
      }
      /**
       * Get the description for the command.
       *
       * @param {Command} cmd
       * @returns {string}
       */
      commandDescription(cmd) {
        return cmd.description();
      }
      /**
       * Get the subcommand summary to show in the list of subcommands.
       * (Fallback to description for backwards compatibility.)
       *
       * @param {Command} cmd
       * @returns {string}
       */
      subcommandDescription(cmd) {
        return cmd.summary() || cmd.description();
      }
      /**
       * Get the option description to show in the list of options.
       *
       * @param {Option} option
       * @return {string}
       */
      optionDescription(option) {
        const extraInfo = [];
        if (option.argChoices) {
          extraInfo.push(
            // use stringify to match the display of the default value
            `choices: ${option.argChoices.map((choice) => JSON.stringify(choice)).join(", ")}`
          );
        }
        if (option.defaultValue !== void 0) {
          const showDefault = option.required || option.optional || option.isBoolean() && typeof option.defaultValue === "boolean";
          if (showDefault) {
            extraInfo.push(
              `default: ${option.defaultValueDescription || JSON.stringify(option.defaultValue)}`
            );
          }
        }
        if (option.presetArg !== void 0 && option.optional) {
          extraInfo.push(`preset: ${JSON.stringify(option.presetArg)}`);
        }
        if (option.envVar !== void 0) {
          extraInfo.push(`env: ${option.envVar}`);
        }
        if (extraInfo.length > 0) {
          return `${option.description} (${extraInfo.join(", ")})`;
        }
        return option.description;
      }
      /**
       * Get the argument description to show in the list of arguments.
       *
       * @param {Argument} argument
       * @return {string}
       */
      argumentDescription(argument) {
        const extraInfo = [];
        if (argument.argChoices) {
          extraInfo.push(
            // use stringify to match the display of the default value
            `choices: ${argument.argChoices.map((choice) => JSON.stringify(choice)).join(", ")}`
          );
        }
        if (argument.defaultValue !== void 0) {
          extraInfo.push(
            `default: ${argument.defaultValueDescription || JSON.stringify(argument.defaultValue)}`
          );
        }
        if (extraInfo.length > 0) {
          const extraDescription = `(${extraInfo.join(", ")})`;
          if (argument.description) {
            return `${argument.description} ${extraDescription}`;
          }
          return extraDescription;
        }
        return argument.description;
      }
      /**
       * Generate the built-in help text.
       *
       * @param {Command} cmd
       * @param {Help} helper
       * @returns {string}
       */
      formatHelp(cmd, helper) {
        const termWidth = helper.padWidth(cmd, helper);
        const helpWidth = helper.helpWidth ?? 80;
        function callFormatItem(term, description) {
          return helper.formatItem(term, termWidth, description, helper);
        }
        let output = [
          `${helper.styleTitle("Usage:")} ${helper.styleUsage(helper.commandUsage(cmd))}`,
          ""
        ];
        const commandDescription = helper.commandDescription(cmd);
        if (commandDescription.length > 0) {
          output = output.concat([
            helper.boxWrap(
              helper.styleCommandDescription(commandDescription),
              helpWidth
            ),
            ""
          ]);
        }
        const argumentList = helper.visibleArguments(cmd).map((argument) => {
          return callFormatItem(
            helper.styleArgumentTerm(helper.argumentTerm(argument)),
            helper.styleArgumentDescription(helper.argumentDescription(argument))
          );
        });
        if (argumentList.length > 0) {
          output = output.concat([
            helper.styleTitle("Arguments:"),
            ...argumentList,
            ""
          ]);
        }
        const optionList = helper.visibleOptions(cmd).map((option) => {
          return callFormatItem(
            helper.styleOptionTerm(helper.optionTerm(option)),
            helper.styleOptionDescription(helper.optionDescription(option))
          );
        });
        if (optionList.length > 0) {
          output = output.concat([
            helper.styleTitle("Options:"),
            ...optionList,
            ""
          ]);
        }
        if (helper.showGlobalOptions) {
          const globalOptionList = helper.visibleGlobalOptions(cmd).map((option) => {
            return callFormatItem(
              helper.styleOptionTerm(helper.optionTerm(option)),
              helper.styleOptionDescription(helper.optionDescription(option))
            );
          });
          if (globalOptionList.length > 0) {
            output = output.concat([
              helper.styleTitle("Global Options:"),
              ...globalOptionList,
              ""
            ]);
          }
        }
        const commandList = helper.visibleCommands(cmd).map((cmd2) => {
          return callFormatItem(
            helper.styleSubcommandTerm(helper.subcommandTerm(cmd2)),
            helper.styleSubcommandDescription(helper.subcommandDescription(cmd2))
          );
        });
        if (commandList.length > 0) {
          output = output.concat([
            helper.styleTitle("Commands:"),
            ...commandList,
            ""
          ]);
        }
        return output.join("\n");
      }
      /**
       * Return display width of string, ignoring ANSI escape sequences. Used in padding and wrapping calculations.
       *
       * @param {string} str
       * @returns {number}
       */
      displayWidth(str) {
        return stripColor(str).length;
      }
      /**
       * Style the title for displaying in the help. Called with 'Usage:', 'Options:', etc.
       *
       * @param {string} str
       * @returns {string}
       */
      styleTitle(str) {
        return str;
      }
      styleUsage(str) {
        return str.split(" ").map((word) => {
          if (word === "[options]") return this.styleOptionText(word);
          if (word === "[command]") return this.styleSubcommandText(word);
          if (word[0] === "[" || word[0] === "<")
            return this.styleArgumentText(word);
          return this.styleCommandText(word);
        }).join(" ");
      }
      styleCommandDescription(str) {
        return this.styleDescriptionText(str);
      }
      styleOptionDescription(str) {
        return this.styleDescriptionText(str);
      }
      styleSubcommandDescription(str) {
        return this.styleDescriptionText(str);
      }
      styleArgumentDescription(str) {
        return this.styleDescriptionText(str);
      }
      styleDescriptionText(str) {
        return str;
      }
      styleOptionTerm(str) {
        return this.styleOptionText(str);
      }
      styleSubcommandTerm(str) {
        return str.split(" ").map((word) => {
          if (word === "[options]") return this.styleOptionText(word);
          if (word[0] === "[" || word[0] === "<")
            return this.styleArgumentText(word);
          return this.styleSubcommandText(word);
        }).join(" ");
      }
      styleArgumentTerm(str) {
        return this.styleArgumentText(str);
      }
      styleOptionText(str) {
        return str;
      }
      styleArgumentText(str) {
        return str;
      }
      styleSubcommandText(str) {
        return str;
      }
      styleCommandText(str) {
        return str;
      }
      /**
       * Calculate the pad width from the maximum term length.
       *
       * @param {Command} cmd
       * @param {Help} helper
       * @returns {number}
       */
      padWidth(cmd, helper) {
        return Math.max(
          helper.longestOptionTermLength(cmd, helper),
          helper.longestGlobalOptionTermLength(cmd, helper),
          helper.longestSubcommandTermLength(cmd, helper),
          helper.longestArgumentTermLength(cmd, helper)
        );
      }
      /**
       * Detect manually wrapped and indented strings by checking for line break followed by whitespace.
       *
       * @param {string} str
       * @returns {boolean}
       */
      preformatted(str) {
        return /\n[^\S\r\n]/.test(str);
      }
      /**
       * Format the "item", which consists of a term and description. Pad the term and wrap the description, indenting the following lines.
       *
       * So "TTT", 5, "DDD DDDD DD DDD" might be formatted for this.helpWidth=17 like so:
       *   TTT  DDD DDDD
       *        DD DDD
       *
       * @param {string} term
       * @param {number} termWidth
       * @param {string} description
       * @param {Help} helper
       * @returns {string}
       */
      formatItem(term, termWidth, description, helper) {
        const itemIndent = 2;
        const itemIndentStr = " ".repeat(itemIndent);
        if (!description) return itemIndentStr + term;
        const paddedTerm = term.padEnd(
          termWidth + term.length - helper.displayWidth(term)
        );
        const spacerWidth = 2;
        const helpWidth = this.helpWidth ?? 80;
        const remainingWidth = helpWidth - termWidth - spacerWidth - itemIndent;
        let formattedDescription;
        if (remainingWidth < this.minWidthToWrap || helper.preformatted(description)) {
          formattedDescription = description;
        } else {
          const wrappedDescription = helper.boxWrap(description, remainingWidth);
          formattedDescription = wrappedDescription.replace(
            /\n/g,
            "\n" + " ".repeat(termWidth + spacerWidth)
          );
        }
        return itemIndentStr + paddedTerm + " ".repeat(spacerWidth) + formattedDescription.replace(/\n/g, `
${itemIndentStr}`);
      }
      /**
       * Wrap a string at whitespace, preserving existing line breaks.
       * Wrapping is skipped if the width is less than `minWidthToWrap`.
       *
       * @param {string} str
       * @param {number} width
       * @returns {string}
       */
      boxWrap(str, width) {
        if (width < this.minWidthToWrap) return str;
        const rawLines = str.split(/\r\n|\n/);
        const chunkPattern = /[\s]*[^\s]+/g;
        const wrappedLines = [];
        rawLines.forEach((line) => {
          const chunks = line.match(chunkPattern);
          if (chunks === null) {
            wrappedLines.push("");
            return;
          }
          let sumChunks = [chunks.shift()];
          let sumWidth = this.displayWidth(sumChunks[0]);
          chunks.forEach((chunk) => {
            const visibleWidth = this.displayWidth(chunk);
            if (sumWidth + visibleWidth <= width) {
              sumChunks.push(chunk);
              sumWidth += visibleWidth;
              return;
            }
            wrappedLines.push(sumChunks.join(""));
            const nextChunk = chunk.trimStart();
            sumChunks = [nextChunk];
            sumWidth = this.displayWidth(nextChunk);
          });
          wrappedLines.push(sumChunks.join(""));
        });
        return wrappedLines.join("\n");
      }
    };
    function stripColor(str) {
      const sgrPattern = /\x1b\[\d*(;\d*)*m/g;
      return str.replace(sgrPattern, "");
    }
    exports2.Help = Help2;
    exports2.stripColor = stripColor;
  }
});

// ../../node_modules/.pnpm/commander@13.1.0/node_modules/commander/lib/option.js
var require_option = __commonJS({
  "../../node_modules/.pnpm/commander@13.1.0/node_modules/commander/lib/option.js"(exports2) {
    "use strict";
    var { InvalidArgumentError: InvalidArgumentError2 } = require_error();
    var Option2 = class {
      /**
       * Initialize a new `Option` with the given `flags` and `description`.
       *
       * @param {string} flags
       * @param {string} [description]
       */
      constructor(flags, description) {
        this.flags = flags;
        this.description = description || "";
        this.required = flags.includes("<");
        this.optional = flags.includes("[");
        this.variadic = /\w\.\.\.[>\]]$/.test(flags);
        this.mandatory = false;
        const optionFlags = splitOptionFlags(flags);
        this.short = optionFlags.shortFlag;
        this.long = optionFlags.longFlag;
        this.negate = false;
        if (this.long) {
          this.negate = this.long.startsWith("--no-");
        }
        this.defaultValue = void 0;
        this.defaultValueDescription = void 0;
        this.presetArg = void 0;
        this.envVar = void 0;
        this.parseArg = void 0;
        this.hidden = false;
        this.argChoices = void 0;
        this.conflictsWith = [];
        this.implied = void 0;
      }
      /**
       * Set the default value, and optionally supply the description to be displayed in the help.
       *
       * @param {*} value
       * @param {string} [description]
       * @return {Option}
       */
      default(value, description) {
        this.defaultValue = value;
        this.defaultValueDescription = description;
        return this;
      }
      /**
       * Preset to use when option used without option-argument, especially optional but also boolean and negated.
       * The custom processing (parseArg) is called.
       *
       * @example
       * new Option('--color').default('GREYSCALE').preset('RGB');
       * new Option('--donate [amount]').preset('20').argParser(parseFloat);
       *
       * @param {*} arg
       * @return {Option}
       */
      preset(arg) {
        this.presetArg = arg;
        return this;
      }
      /**
       * Add option name(s) that conflict with this option.
       * An error will be displayed if conflicting options are found during parsing.
       *
       * @example
       * new Option('--rgb').conflicts('cmyk');
       * new Option('--js').conflicts(['ts', 'jsx']);
       *
       * @param {(string | string[])} names
       * @return {Option}
       */
      conflicts(names) {
        this.conflictsWith = this.conflictsWith.concat(names);
        return this;
      }
      /**
       * Specify implied option values for when this option is set and the implied options are not.
       *
       * The custom processing (parseArg) is not called on the implied values.
       *
       * @example
       * program
       *   .addOption(new Option('--log', 'write logging information to file'))
       *   .addOption(new Option('--trace', 'log extra details').implies({ log: 'trace.txt' }));
       *
       * @param {object} impliedOptionValues
       * @return {Option}
       */
      implies(impliedOptionValues) {
        let newImplied = impliedOptionValues;
        if (typeof impliedOptionValues === "string") {
          newImplied = { [impliedOptionValues]: true };
        }
        this.implied = Object.assign(this.implied || {}, newImplied);
        return this;
      }
      /**
       * Set environment variable to check for option value.
       *
       * An environment variable is only used if when processed the current option value is
       * undefined, or the source of the current value is 'default' or 'config' or 'env'.
       *
       * @param {string} name
       * @return {Option}
       */
      env(name) {
        this.envVar = name;
        return this;
      }
      /**
       * Set the custom handler for processing CLI option arguments into option values.
       *
       * @param {Function} [fn]
       * @return {Option}
       */
      argParser(fn) {
        this.parseArg = fn;
        return this;
      }
      /**
       * Whether the option is mandatory and must have a value after parsing.
       *
       * @param {boolean} [mandatory=true]
       * @return {Option}
       */
      makeOptionMandatory(mandatory = true) {
        this.mandatory = !!mandatory;
        return this;
      }
      /**
       * Hide option in help.
       *
       * @param {boolean} [hide=true]
       * @return {Option}
       */
      hideHelp(hide = true) {
        this.hidden = !!hide;
        return this;
      }
      /**
       * @package
       */
      _concatValue(value, previous) {
        if (previous === this.defaultValue || !Array.isArray(previous)) {
          return [value];
        }
        return previous.concat(value);
      }
      /**
       * Only allow option value to be one of choices.
       *
       * @param {string[]} values
       * @return {Option}
       */
      choices(values) {
        this.argChoices = values.slice();
        this.parseArg = (arg, previous) => {
          if (!this.argChoices.includes(arg)) {
            throw new InvalidArgumentError2(
              `Allowed choices are ${this.argChoices.join(", ")}.`
            );
          }
          if (this.variadic) {
            return this._concatValue(arg, previous);
          }
          return arg;
        };
        return this;
      }
      /**
       * Return option name.
       *
       * @return {string}
       */
      name() {
        if (this.long) {
          return this.long.replace(/^--/, "");
        }
        return this.short.replace(/^-/, "");
      }
      /**
       * Return option name, in a camelcase format that can be used
       * as an object attribute key.
       *
       * @return {string}
       */
      attributeName() {
        if (this.negate) {
          return camelcase(this.name().replace(/^no-/, ""));
        }
        return camelcase(this.name());
      }
      /**
       * Check if `arg` matches the short or long flag.
       *
       * @param {string} arg
       * @return {boolean}
       * @package
       */
      is(arg) {
        return this.short === arg || this.long === arg;
      }
      /**
       * Return whether a boolean option.
       *
       * Options are one of boolean, negated, required argument, or optional argument.
       *
       * @return {boolean}
       * @package
       */
      isBoolean() {
        return !this.required && !this.optional && !this.negate;
      }
    };
    var DualOptions = class {
      /**
       * @param {Option[]} options
       */
      constructor(options) {
        this.positiveOptions = /* @__PURE__ */ new Map();
        this.negativeOptions = /* @__PURE__ */ new Map();
        this.dualOptions = /* @__PURE__ */ new Set();
        options.forEach((option) => {
          if (option.negate) {
            this.negativeOptions.set(option.attributeName(), option);
          } else {
            this.positiveOptions.set(option.attributeName(), option);
          }
        });
        this.negativeOptions.forEach((value, key) => {
          if (this.positiveOptions.has(key)) {
            this.dualOptions.add(key);
          }
        });
      }
      /**
       * Did the value come from the option, and not from possible matching dual option?
       *
       * @param {*} value
       * @param {Option} option
       * @returns {boolean}
       */
      valueFromOption(value, option) {
        const optionKey = option.attributeName();
        if (!this.dualOptions.has(optionKey)) return true;
        const preset = this.negativeOptions.get(optionKey).presetArg;
        const negativeValue = preset !== void 0 ? preset : false;
        return option.negate === (negativeValue === value);
      }
    };
    function camelcase(str) {
      return str.split("-").reduce((str2, word) => {
        return str2 + word[0].toUpperCase() + word.slice(1);
      });
    }
    function splitOptionFlags(flags) {
      let shortFlag;
      let longFlag;
      const shortFlagExp = /^-[^-]$/;
      const longFlagExp = /^--[^-]/;
      const flagParts = flags.split(/[ |,]+/).concat("guard");
      if (shortFlagExp.test(flagParts[0])) shortFlag = flagParts.shift();
      if (longFlagExp.test(flagParts[0])) longFlag = flagParts.shift();
      if (!shortFlag && shortFlagExp.test(flagParts[0]))
        shortFlag = flagParts.shift();
      if (!shortFlag && longFlagExp.test(flagParts[0])) {
        shortFlag = longFlag;
        longFlag = flagParts.shift();
      }
      if (flagParts[0].startsWith("-")) {
        const unsupportedFlag = flagParts[0];
        const baseError = `option creation failed due to '${unsupportedFlag}' in option flags '${flags}'`;
        if (/^-[^-][^-]/.test(unsupportedFlag))
          throw new Error(
            `${baseError}
- a short flag is a single dash and a single character
  - either use a single dash and a single character (for a short flag)
  - or use a double dash for a long option (and can have two, like '--ws, --workspace')`
          );
        if (shortFlagExp.test(unsupportedFlag))
          throw new Error(`${baseError}
- too many short flags`);
        if (longFlagExp.test(unsupportedFlag))
          throw new Error(`${baseError}
- too many long flags`);
        throw new Error(`${baseError}
- unrecognised flag format`);
      }
      if (shortFlag === void 0 && longFlag === void 0)
        throw new Error(
          `option creation failed due to no flags found in '${flags}'.`
        );
      return { shortFlag, longFlag };
    }
    exports2.Option = Option2;
    exports2.DualOptions = DualOptions;
  }
});

// ../../node_modules/.pnpm/commander@13.1.0/node_modules/commander/lib/suggestSimilar.js
var require_suggestSimilar = __commonJS({
  "../../node_modules/.pnpm/commander@13.1.0/node_modules/commander/lib/suggestSimilar.js"(exports2) {
    "use strict";
    var maxDistance = 3;
    function editDistance(a, b) {
      if (Math.abs(a.length - b.length) > maxDistance)
        return Math.max(a.length, b.length);
      const d = [];
      for (let i = 0; i <= a.length; i++) {
        d[i] = [i];
      }
      for (let j = 0; j <= b.length; j++) {
        d[0][j] = j;
      }
      for (let j = 1; j <= b.length; j++) {
        for (let i = 1; i <= a.length; i++) {
          let cost = 1;
          if (a[i - 1] === b[j - 1]) {
            cost = 0;
          } else {
            cost = 1;
          }
          d[i][j] = Math.min(
            d[i - 1][j] + 1,
            // deletion
            d[i][j - 1] + 1,
            // insertion
            d[i - 1][j - 1] + cost
            // substitution
          );
          if (i > 1 && j > 1 && a[i - 1] === b[j - 2] && a[i - 2] === b[j - 1]) {
            d[i][j] = Math.min(d[i][j], d[i - 2][j - 2] + 1);
          }
        }
      }
      return d[a.length][b.length];
    }
    function suggestSimilar(word, candidates) {
      if (!candidates || candidates.length === 0) return "";
      candidates = Array.from(new Set(candidates));
      const searchingOptions = word.startsWith("--");
      if (searchingOptions) {
        word = word.slice(2);
        candidates = candidates.map((candidate) => candidate.slice(2));
      }
      let similar = [];
      let bestDistance = maxDistance;
      const minSimilarity = 0.4;
      candidates.forEach((candidate) => {
        if (candidate.length <= 1) return;
        const distance = editDistance(word, candidate);
        const length = Math.max(word.length, candidate.length);
        const similarity = (length - distance) / length;
        if (similarity > minSimilarity) {
          if (distance < bestDistance) {
            bestDistance = distance;
            similar = [candidate];
          } else if (distance === bestDistance) {
            similar.push(candidate);
          }
        }
      });
      similar.sort((a, b) => a.localeCompare(b));
      if (searchingOptions) {
        similar = similar.map((candidate) => `--${candidate}`);
      }
      if (similar.length > 1) {
        return `
(Did you mean one of ${similar.join(", ")}?)`;
      }
      if (similar.length === 1) {
        return `
(Did you mean ${similar[0]}?)`;
      }
      return "";
    }
    exports2.suggestSimilar = suggestSimilar;
  }
});

// ../../node_modules/.pnpm/commander@13.1.0/node_modules/commander/lib/command.js
var require_command = __commonJS({
  "../../node_modules/.pnpm/commander@13.1.0/node_modules/commander/lib/command.js"(exports2) {
    "use strict";
    var EventEmitter = require("events").EventEmitter;
    var childProcess = require("child_" + "process");
    var path = require("path");
    var fs = require("fs");
    var process2 = require("process");
    var { Argument: Argument2, humanReadableArgName } = require_argument();
    var { CommanderError: CommanderError2 } = require_error();
    var { Help: Help2, stripColor } = require_help();
    var { Option: Option2, DualOptions } = require_option();
    var { suggestSimilar } = require_suggestSimilar();
    function runChild(childProcess2, command, args, options) {
      const method = ["sp", "awn"].join("");
      return childProcess2[method](command, args, options);
    }
    var Command2 = class _Command extends EventEmitter {
      /**
       * Initialize a new `Command`.
       *
       * @param {string} [name]
       */
      constructor(name) {
        super();
        this.commands = [];
        this.options = [];
        this.parent = null;
        this._allowUnknownOption = false;
        this._allowExcessArguments = false;
        this.registeredArguments = [];
        this._args = this.registeredArguments;
        this.args = [];
        this.rawArgs = [];
        this.processedArgs = [];
        this._scriptPath = null;
        this._name = name || "";
        this._optionValues = {};
        this._optionValueSources = {};
        this._storeOptionsAsProperties = false;
        this._actionHandler = null;
        this._executableHandler = false;
        this._executableFile = null;
        this._executableDir = null;
        this._defaultCommandName = null;
        this._exitCallback = null;
        this._aliases = [];
        this._combineFlagAndOptionalValue = true;
        this._description = "";
        this._summary = "";
        this._argsDescription = void 0;
        this._enablePositionalOptions = false;
        this._passThroughOptions = false;
        this._lifeCycleHooks = {};
        this._showHelpAfterError = false;
        this._showSuggestionAfterError = true;
        this._savedState = null;
        this._outputConfiguration = {
          writeOut: (str) => process2.stdout.write(str),
          writeErr: (str) => process2.stderr.write(str),
          outputError: (str, write) => write(str),
          getOutHelpWidth: () => process2.stdout.isTTY ? process2.stdout.columns : void 0,
          getErrHelpWidth: () => process2.stderr.isTTY ? process2.stderr.columns : void 0,
          getOutHasColors: () => useColor() ?? (process2.stdout.isTTY && process2.stdout.hasColors?.()),
          getErrHasColors: () => useColor() ?? (process2.stderr.isTTY && process2.stderr.hasColors?.()),
          stripColor: (str) => stripColor(str)
        };
        this._hidden = false;
        this._helpOption = void 0;
        this._addImplicitHelpCommand = void 0;
        this._helpCommand = void 0;
        this._helpConfiguration = {};
      }
      /**
       * Copy settings that are useful to have in common across root command and subcommands.
       *
       * (Used internally when adding a command using `.command()` so subcommands inherit parent settings.)
       *
       * @param {Command} sourceCommand
       * @return {Command} `this` command for chaining
       */
      copyInheritedSettings(sourceCommand) {
        this._outputConfiguration = sourceCommand._outputConfiguration;
        this._helpOption = sourceCommand._helpOption;
        this._helpCommand = sourceCommand._helpCommand;
        this._helpConfiguration = sourceCommand._helpConfiguration;
        this._exitCallback = sourceCommand._exitCallback;
        this._storeOptionsAsProperties = sourceCommand._storeOptionsAsProperties;
        this._combineFlagAndOptionalValue = sourceCommand._combineFlagAndOptionalValue;
        this._allowExcessArguments = sourceCommand._allowExcessArguments;
        this._enablePositionalOptions = sourceCommand._enablePositionalOptions;
        this._showHelpAfterError = sourceCommand._showHelpAfterError;
        this._showSuggestionAfterError = sourceCommand._showSuggestionAfterError;
        return this;
      }
      /**
       * @returns {Command[]}
       * @private
       */
      _getCommandAndAncestors() {
        const result = [];
        for (let command = this; command; command = command.parent) {
          result.push(command);
        }
        return result;
      }
      /**
       * Define a command.
       *
       * There are two styles of command: pay attention to where to put the description.
       *
       * @example
       * // Command implemented using action handler (description is supplied separately to `.command`)
       * program
       *   .command('clone <source> [destination]')
       *   .description('clone a repository into a newly created directory')
       *   .action((source, destination) => {
       *     console.log('clone command called');
       *   });
       *
       * // Command implemented using separate executable file (description is second parameter to `.command`)
       * program
       *   .command('start <service>', 'start named service')
       *   .command('stop [service]', 'stop named service, or all if no name supplied');
       *
       * @param {string} nameAndArgs - command name and arguments, args are `<required>` or `[optional]` and last may also be `variadic...`
       * @param {(object | string)} [actionOptsOrExecDesc] - configuration options (for action), or description (for executable)
       * @param {object} [execOpts] - configuration options (for executable)
       * @return {Command} returns new command for action handler, or `this` for executable command
       */
      command(nameAndArgs, actionOptsOrExecDesc, execOpts) {
        let desc = actionOptsOrExecDesc;
        let opts = execOpts;
        if (typeof desc === "object" && desc !== null) {
          opts = desc;
          desc = null;
        }
        opts = opts || {};
        const [, name, args] = nameAndArgs.match(/([^ ]+) *(.*)/);
        const cmd = this.createCommand(name);
        if (desc) {
          cmd.description(desc);
          cmd._executableHandler = true;
        }
        if (opts.isDefault) this._defaultCommandName = cmd._name;
        cmd._hidden = !!(opts.noHelp || opts.hidden);
        cmd._executableFile = opts.executableFile || null;
        if (args) cmd.arguments(args);
        this._registerCommand(cmd);
        cmd.parent = this;
        cmd.copyInheritedSettings(this);
        if (desc) return this;
        return cmd;
      }
      /**
       * Factory routine to create a new unattached command.
       *
       * See .command() for creating an attached subcommand, which uses this routine to
       * create the command. You can override createCommand to customise subcommands.
       *
       * @param {string} [name]
       * @return {Command} new command
       */
      createCommand(name) {
        return new _Command(name);
      }
      /**
       * You can customise the help with a subclass of Help by overriding createHelp,
       * or by overriding Help properties using configureHelp().
       *
       * @return {Help}
       */
      createHelp() {
        return Object.assign(new Help2(), this.configureHelp());
      }
      /**
       * You can customise the help by overriding Help properties using configureHelp(),
       * or with a subclass of Help by overriding createHelp().
       *
       * @param {object} [configuration] - configuration options
       * @return {(Command | object)} `this` command for chaining, or stored configuration
       */
      configureHelp(configuration) {
        if (configuration === void 0) return this._helpConfiguration;
        this._helpConfiguration = configuration;
        return this;
      }
      /**
       * The default output goes to stdout and stderr. You can customise this for special
       * applications. You can also customise the display of errors by overriding outputError.
       *
       * The configuration properties are all functions:
       *
       *     // change how output being written, defaults to stdout and stderr
       *     writeOut(str)
       *     writeErr(str)
       *     // change how output being written for errors, defaults to writeErr
       *     outputError(str, write) // used for displaying errors and not used for displaying help
       *     // specify width for wrapping help
       *     getOutHelpWidth()
       *     getErrHelpWidth()
       *     // color support, currently only used with Help
       *     getOutHasColors()
       *     getErrHasColors()
       *     stripColor() // used to remove ANSI escape codes if output does not have colors
       *
       * @param {object} [configuration] - configuration options
       * @return {(Command | object)} `this` command for chaining, or stored configuration
       */
      configureOutput(configuration) {
        if (configuration === void 0) return this._outputConfiguration;
        Object.assign(this._outputConfiguration, configuration);
        return this;
      }
      /**
       * Display the help or a custom message after an error occurs.
       *
       * @param {(boolean|string)} [displayHelp]
       * @return {Command} `this` command for chaining
       */
      showHelpAfterError(displayHelp = true) {
        if (typeof displayHelp !== "string") displayHelp = !!displayHelp;
        this._showHelpAfterError = displayHelp;
        return this;
      }
      /**
       * Display suggestion of similar commands for unknown commands, or options for unknown options.
       *
       * @param {boolean} [displaySuggestion]
       * @return {Command} `this` command for chaining
       */
      showSuggestionAfterError(displaySuggestion = true) {
        this._showSuggestionAfterError = !!displaySuggestion;
        return this;
      }
      /**
       * Add a prepared subcommand.
       *
       * See .command() for creating an attached subcommand which inherits settings from its parent.
       *
       * @param {Command} cmd - new subcommand
       * @param {object} [opts] - configuration options
       * @return {Command} `this` command for chaining
       */
      addCommand(cmd, opts) {
        if (!cmd._name) {
          throw new Error(`Command passed to .addCommand() must have a name
- specify the name in Command constructor or using .name()`);
        }
        opts = opts || {};
        if (opts.isDefault) this._defaultCommandName = cmd._name;
        if (opts.noHelp || opts.hidden) cmd._hidden = true;
        this._registerCommand(cmd);
        cmd.parent = this;
        cmd._checkForBrokenPassThrough();
        return this;
      }
      /**
       * Factory routine to create a new unattached argument.
       *
       * See .argument() for creating an attached argument, which uses this routine to
       * create the argument. You can override createArgument to return a custom argument.
       *
       * @param {string} name
       * @param {string} [description]
       * @return {Argument} new argument
       */
      createArgument(name, description) {
        return new Argument2(name, description);
      }
      /**
       * Define argument syntax for command.
       *
       * The default is that the argument is required, and you can explicitly
       * indicate this with <> around the name. Put [] around the name for an optional argument.
       *
       * @example
       * program.argument('<input-file>');
       * program.argument('[output-file]');
       *
       * @param {string} name
       * @param {string} [description]
       * @param {(Function|*)} [fn] - custom argument processing function
       * @param {*} [defaultValue]
       * @return {Command} `this` command for chaining
       */
      argument(name, description, fn, defaultValue) {
        const argument = this.createArgument(name, description);
        if (typeof fn === "function") {
          argument.default(defaultValue).argParser(fn);
        } else {
          argument.default(fn);
        }
        this.addArgument(argument);
        return this;
      }
      /**
       * Define argument syntax for command, adding multiple at once (without descriptions).
       *
       * See also .argument().
       *
       * @example
       * program.arguments('<cmd> [env]');
       *
       * @param {string} names
       * @return {Command} `this` command for chaining
       */
      arguments(names) {
        names.trim().split(/ +/).forEach((detail) => {
          this.argument(detail);
        });
        return this;
      }
      /**
       * Define argument syntax for command, adding a prepared argument.
       *
       * @param {Argument} argument
       * @return {Command} `this` command for chaining
       */
      addArgument(argument) {
        const previousArgument = this.registeredArguments.slice(-1)[0];
        if (previousArgument && previousArgument.variadic) {
          throw new Error(
            `only the last argument can be variadic '${previousArgument.name()}'`
          );
        }
        if (argument.required && argument.defaultValue !== void 0 && argument.parseArg === void 0) {
          throw new Error(
            `a default value for a required argument is never used: '${argument.name()}'`
          );
        }
        this.registeredArguments.push(argument);
        return this;
      }
      /**
       * Customise or override default help command. By default a help command is automatically added if your command has subcommands.
       *
       * @example
       *    program.helpCommand('help [cmd]');
       *    program.helpCommand('help [cmd]', 'show help');
       *    program.helpCommand(false); // suppress default help command
       *    program.helpCommand(true); // add help command even if no subcommands
       *
       * @param {string|boolean} enableOrNameAndArgs - enable with custom name and/or arguments, or boolean to override whether added
       * @param {string} [description] - custom description
       * @return {Command} `this` command for chaining
       */
      helpCommand(enableOrNameAndArgs, description) {
        if (typeof enableOrNameAndArgs === "boolean") {
          this._addImplicitHelpCommand = enableOrNameAndArgs;
          return this;
        }
        enableOrNameAndArgs = enableOrNameAndArgs ?? "help [command]";
        const [, helpName, helpArgs] = enableOrNameAndArgs.match(/([^ ]+) *(.*)/);
        const helpDescription = description ?? "display help for command";
        const helpCommand = this.createCommand(helpName);
        helpCommand.helpOption(false);
        if (helpArgs) helpCommand.arguments(helpArgs);
        if (helpDescription) helpCommand.description(helpDescription);
        this._addImplicitHelpCommand = true;
        this._helpCommand = helpCommand;
        return this;
      }
      /**
       * Add prepared custom help command.
       *
       * @param {(Command|string|boolean)} helpCommand - custom help command, or deprecated enableOrNameAndArgs as for `.helpCommand()`
       * @param {string} [deprecatedDescription] - deprecated custom description used with custom name only
       * @return {Command} `this` command for chaining
       */
      addHelpCommand(helpCommand, deprecatedDescription) {
        if (typeof helpCommand !== "object") {
          this.helpCommand(helpCommand, deprecatedDescription);
          return this;
        }
        this._addImplicitHelpCommand = true;
        this._helpCommand = helpCommand;
        return this;
      }
      /**
       * Lazy create help command.
       *
       * @return {(Command|null)}
       * @package
       */
      _getHelpCommand() {
        const hasImplicitHelpCommand = this._addImplicitHelpCommand ?? (this.commands.length && !this._actionHandler && !this._findCommand("help"));
        if (hasImplicitHelpCommand) {
          if (this._helpCommand === void 0) {
            this.helpCommand(void 0, void 0);
          }
          return this._helpCommand;
        }
        return null;
      }
      /**
       * Add hook for life cycle event.
       *
       * @param {string} event
       * @param {Function} listener
       * @return {Command} `this` command for chaining
       */
      hook(event, listener) {
        const allowedValues = ["preSubcommand", "preAction", "postAction"];
        if (!allowedValues.includes(event)) {
          throw new Error(`Unexpected value for event passed to hook : '${event}'.
Expecting one of '${allowedValues.join("', '")}'`);
        }
        if (this._lifeCycleHooks[event]) {
          this._lifeCycleHooks[event].push(listener);
        } else {
          this._lifeCycleHooks[event] = [listener];
        }
        return this;
      }
      /**
       * Register callback to use as replacement for calling process.exit.
       *
       * @param {Function} [fn] optional callback which will be passed a CommanderError, defaults to throwing
       * @return {Command} `this` command for chaining
       */
      exitOverride(fn) {
        if (fn) {
          this._exitCallback = fn;
        } else {
          this._exitCallback = (err) => {
            if (err.code !== "commander.executeSubCommandAsync") {
              throw err;
            } else {
            }
          };
        }
        return this;
      }
      /**
       * Call process.exit, and _exitCallback if defined.
       *
       * @param {number} exitCode exit code for using with process.exit
       * @param {string} code an id string representing the error
       * @param {string} message human-readable description of the error
       * @return never
       * @private
       */
      _exit(exitCode, code, message) {
        if (this._exitCallback) {
          this._exitCallback(new CommanderError2(exitCode, code, message));
        }
        process2.exit(exitCode);
      }
      /**
       * Register callback `fn` for the command.
       *
       * @example
       * program
       *   .command('serve')
       *   .description('start service')
       *   .action(function() {
       *      // do work here
       *   });
       *
       * @param {Function} fn
       * @return {Command} `this` command for chaining
       */
      action(fn) {
        const listener = (args) => {
          const expectedArgsCount = this.registeredArguments.length;
          const actionArgs = args.slice(0, expectedArgsCount);
          if (this._storeOptionsAsProperties) {
            actionArgs[expectedArgsCount] = this;
          } else {
            actionArgs[expectedArgsCount] = this.opts();
          }
          actionArgs.push(this);
          return fn.apply(this, actionArgs);
        };
        this._actionHandler = listener;
        return this;
      }
      /**
       * Factory routine to create a new unattached option.
       *
       * See .option() for creating an attached option, which uses this routine to
       * create the option. You can override createOption to return a custom option.
       *
       * @param {string} flags
       * @param {string} [description]
       * @return {Option} new option
       */
      createOption(flags, description) {
        return new Option2(flags, description);
      }
      /**
       * Wrap parseArgs to catch 'commander.invalidArgument'.
       *
       * @param {(Option | Argument)} target
       * @param {string} value
       * @param {*} previous
       * @param {string} invalidArgumentMessage
       * @private
       */
      _callParseArg(target, value, previous, invalidArgumentMessage) {
        try {
          return target.parseArg(value, previous);
        } catch (err) {
          if (err.code === "commander.invalidArgument") {
            const message = `${invalidArgumentMessage} ${err.message}`;
            this.error(message, { exitCode: err.exitCode, code: err.code });
          }
          throw err;
        }
      }
      /**
       * Check for option flag conflicts.
       * Register option if no conflicts found, or throw on conflict.
       *
       * @param {Option} option
       * @private
       */
      _registerOption(option) {
        const matchingOption = option.short && this._findOption(option.short) || option.long && this._findOption(option.long);
        if (matchingOption) {
          const matchingFlag = option.long && this._findOption(option.long) ? option.long : option.short;
          throw new Error(`Cannot add option '${option.flags}'${this._name && ` to command '${this._name}'`} due to conflicting flag '${matchingFlag}'
-  already used by option '${matchingOption.flags}'`);
        }
        this.options.push(option);
      }
      /**
       * Check for command name and alias conflicts with existing commands.
       * Register command if no conflicts found, or throw on conflict.
       *
       * @param {Command} command
       * @private
       */
      _registerCommand(command) {
        const knownBy = (cmd) => {
          return [cmd.name()].concat(cmd.aliases());
        };
        const alreadyUsed = knownBy(command).find(
          (name) => this._findCommand(name)
        );
        if (alreadyUsed) {
          const existingCmd = knownBy(this._findCommand(alreadyUsed)).join("|");
          const newCmd = knownBy(command).join("|");
          throw new Error(
            `cannot add command '${newCmd}' as already have command '${existingCmd}'`
          );
        }
        this.commands.push(command);
      }
      /**
       * Add an option.
       *
       * @param {Option} option
       * @return {Command} `this` command for chaining
       */
      addOption(option) {
        this._registerOption(option);
        const oname = option.name();
        const name = option.attributeName();
        if (option.negate) {
          const positiveLongFlag = option.long.replace(/^--no-/, "--");
          if (!this._findOption(positiveLongFlag)) {
            this.setOptionValueWithSource(
              name,
              option.defaultValue === void 0 ? true : option.defaultValue,
              "default"
            );
          }
        } else if (option.defaultValue !== void 0) {
          this.setOptionValueWithSource(name, option.defaultValue, "default");
        }
        const handleOptionValue = (val, invalidValueMessage, valueSource) => {
          if (val == null && option.presetArg !== void 0) {
            val = option.presetArg;
          }
          const oldValue = this.getOptionValue(name);
          if (val !== null && option.parseArg) {
            val = this._callParseArg(option, val, oldValue, invalidValueMessage);
          } else if (val !== null && option.variadic) {
            val = option._concatValue(val, oldValue);
          }
          if (val == null) {
            if (option.negate) {
              val = false;
            } else if (option.isBoolean() || option.optional) {
              val = true;
            } else {
              val = "";
            }
          }
          this.setOptionValueWithSource(name, val, valueSource);
        };
        this.on("option:" + oname, (val) => {
          const invalidValueMessage = `error: option '${option.flags}' argument '${val}' is invalid.`;
          handleOptionValue(val, invalidValueMessage, "cli");
        });
        if (option.envVar) {
          this.on("optionEnv:" + oname, (val) => {
            const invalidValueMessage = `error: option '${option.flags}' value '${val}' from env '${option.envVar}' is invalid.`;
            handleOptionValue(val, invalidValueMessage, "env");
          });
        }
        return this;
      }
      /**
       * Internal implementation shared by .option() and .requiredOption()
       *
       * @return {Command} `this` command for chaining
       * @private
       */
      _optionEx(config, flags, description, fn, defaultValue) {
        if (typeof flags === "object" && flags instanceof Option2) {
          throw new Error(
            "To add an Option object use addOption() instead of option() or requiredOption()"
          );
        }
        const option = this.createOption(flags, description);
        option.makeOptionMandatory(!!config.mandatory);
        if (typeof fn === "function") {
          option.default(defaultValue).argParser(fn);
        } else if (fn instanceof RegExp) {
          const regex = fn;
          fn = (val, def) => {
            const m = String(val).match(regex);
            return m ? m[0] : def;
          };
          option.default(defaultValue).argParser(fn);
        } else {
          option.default(fn);
        }
        return this.addOption(option);
      }
      /**
       * Define option with `flags`, `description`, and optional argument parsing function or `defaultValue` or both.
       *
       * The `flags` string contains the short and/or long flags, separated by comma, a pipe or space. A required
       * option-argument is indicated by `<>` and an optional option-argument by `[]`.
       *
       * See the README for more details, and see also addOption() and requiredOption().
       *
       * @example
       * program
       *     .option('-p, --pepper', 'add pepper')
       *     .option('--pt, --pizza-type <TYPE>', 'type of pizza') // required option-argument
       *     .option('-c, --cheese [CHEESE]', 'add extra cheese', 'mozzarella') // optional option-argument with default
       *     .option('-t, --tip <VALUE>', 'add tip to purchase cost', parseFloat) // custom parse function
       *
       * @param {string} flags
       * @param {string} [description]
       * @param {(Function|*)} [parseArg] - custom option processing function or default value
       * @param {*} [defaultValue]
       * @return {Command} `this` command for chaining
       */
      option(flags, description, parseArg, defaultValue) {
        return this._optionEx({}, flags, description, parseArg, defaultValue);
      }
      /**
       * Add a required option which must have a value after parsing. This usually means
       * the option must be specified on the command line. (Otherwise the same as .option().)
       *
       * The `flags` string contains the short and/or long flags, separated by comma, a pipe or space.
       *
       * @param {string} flags
       * @param {string} [description]
       * @param {(Function|*)} [parseArg] - custom option processing function or default value
       * @param {*} [defaultValue]
       * @return {Command} `this` command for chaining
       */
      requiredOption(flags, description, parseArg, defaultValue) {
        return this._optionEx(
          { mandatory: true },
          flags,
          description,
          parseArg,
          defaultValue
        );
      }
      /**
       * Alter parsing of short flags with optional values.
       *
       * @example
       * // for `.option('-f,--flag [value]'):
       * program.combineFlagAndOptionalValue(true);  // `-f80` is treated like `--flag=80`, this is the default behaviour
       * program.combineFlagAndOptionalValue(false) // `-fb` is treated like `-f -b`
       *
       * @param {boolean} [combine] - if `true` or omitted, an optional value can be specified directly after the flag.
       * @return {Command} `this` command for chaining
       */
      combineFlagAndOptionalValue(combine = true) {
        this._combineFlagAndOptionalValue = !!combine;
        return this;
      }
      /**
       * Allow unknown options on the command line.
       *
       * @param {boolean} [allowUnknown] - if `true` or omitted, no error will be thrown for unknown options.
       * @return {Command} `this` command for chaining
       */
      allowUnknownOption(allowUnknown = true) {
        this._allowUnknownOption = !!allowUnknown;
        return this;
      }
      /**
       * Allow excess command-arguments on the command line. Pass false to make excess arguments an error.
       *
       * @param {boolean} [allowExcess] - if `true` or omitted, no error will be thrown for excess arguments.
       * @return {Command} `this` command for chaining
       */
      allowExcessArguments(allowExcess = true) {
        this._allowExcessArguments = !!allowExcess;
        return this;
      }
      /**
       * Enable positional options. Positional means global options are specified before subcommands which lets
       * subcommands reuse the same option names, and also enables subcommands to turn on passThroughOptions.
       * The default behaviour is non-positional and global options may appear anywhere on the command line.
       *
       * @param {boolean} [positional]
       * @return {Command} `this` command for chaining
       */
      enablePositionalOptions(positional = true) {
        this._enablePositionalOptions = !!positional;
        return this;
      }
      /**
       * Pass through options that come after command-arguments rather than treat them as command-options,
       * so actual command-options come before command-arguments. Turning this on for a subcommand requires
       * positional options to have been enabled on the program (parent commands).
       * The default behaviour is non-positional and options may appear before or after command-arguments.
       *
       * @param {boolean} [passThrough] for unknown options.
       * @return {Command} `this` command for chaining
       */
      passThroughOptions(passThrough = true) {
        this._passThroughOptions = !!passThrough;
        this._checkForBrokenPassThrough();
        return this;
      }
      /**
       * @private
       */
      _checkForBrokenPassThrough() {
        if (this.parent && this._passThroughOptions && !this.parent._enablePositionalOptions) {
          throw new Error(
            `passThroughOptions cannot be used for '${this._name}' without turning on enablePositionalOptions for parent command(s)`
          );
        }
      }
      /**
       * Whether to store option values as properties on command object,
       * or store separately (specify false). In both cases the option values can be accessed using .opts().
       *
       * @param {boolean} [storeAsProperties=true]
       * @return {Command} `this` command for chaining
       */
      storeOptionsAsProperties(storeAsProperties = true) {
        if (this.options.length) {
          throw new Error("call .storeOptionsAsProperties() before adding options");
        }
        if (Object.keys(this._optionValues).length) {
          throw new Error(
            "call .storeOptionsAsProperties() before setting option values"
          );
        }
        this._storeOptionsAsProperties = !!storeAsProperties;
        return this;
      }
      /**
       * Retrieve option value.
       *
       * @param {string} key
       * @return {object} value
       */
      getOptionValue(key) {
        if (this._storeOptionsAsProperties) {
          return this[key];
        }
        return this._optionValues[key];
      }
      /**
       * Store option value.
       *
       * @param {string} key
       * @param {object} value
       * @return {Command} `this` command for chaining
       */
      setOptionValue(key, value) {
        return this.setOptionValueWithSource(key, value, void 0);
      }
      /**
       * Store option value and where the value came from.
       *
       * @param {string} key
       * @param {object} value
       * @param {string} source - expected values are default/config/env/cli/implied
       * @return {Command} `this` command for chaining
       */
      setOptionValueWithSource(key, value, source) {
        if (this._storeOptionsAsProperties) {
          this[key] = value;
        } else {
          this._optionValues[key] = value;
        }
        this._optionValueSources[key] = source;
        return this;
      }
      /**
       * Get source of option value.
       * Expected values are default | config | env | cli | implied
       *
       * @param {string} key
       * @return {string}
       */
      getOptionValueSource(key) {
        return this._optionValueSources[key];
      }
      /**
       * Get source of option value. See also .optsWithGlobals().
       * Expected values are default | config | env | cli | implied
       *
       * @param {string} key
       * @return {string}
       */
      getOptionValueSourceWithGlobals(key) {
        let source;
        this._getCommandAndAncestors().forEach((cmd) => {
          if (cmd.getOptionValueSource(key) !== void 0) {
            source = cmd.getOptionValueSource(key);
          }
        });
        return source;
      }
      /**
       * Get user arguments from implied or explicit arguments.
       * Side-effects: set _scriptPath if args included script. Used for default program name, and subcommand searches.
       *
       * @private
       */
      _prepareUserArgs(argv, parseOptions) {
        if (argv !== void 0 && !Array.isArray(argv)) {
          throw new Error("first parameter to parse must be array or undefined");
        }
        parseOptions = parseOptions || {};
        if (argv === void 0 && parseOptions.from === void 0) {
          if (process2.versions?.electron) {
            parseOptions.from = "electron";
          }
          const execArgv = process2.execArgv ?? [];
          if (execArgv.includes("-e") || execArgv.includes("--eval") || execArgv.includes("-p") || execArgv.includes("--print")) {
            parseOptions.from = "eval";
          }
        }
        if (argv === void 0) {
          argv = process2.argv;
        }
        this.rawArgs = argv.slice();
        let userArgs;
        switch (parseOptions.from) {
          case void 0:
          case "node":
            this._scriptPath = argv[1];
            userArgs = argv.slice(2);
            break;
          case "electron":
            if (process2.defaultApp) {
              this._scriptPath = argv[1];
              userArgs = argv.slice(2);
            } else {
              userArgs = argv.slice(1);
            }
            break;
          case "user":
            userArgs = argv.slice(0);
            break;
          case "eval":
            userArgs = argv.slice(1);
            break;
          default:
            throw new Error(
              `unexpected parse option { from: '${parseOptions.from}' }`
            );
        }
        if (!this._name && this._scriptPath)
          this.nameFromFilename(this._scriptPath);
        this._name = this._name || "program";
        return userArgs;
      }
      /**
       * Parse `argv`, setting options and invoking commands when defined.
       *
       * Use parseAsync instead of parse if any of your action handlers are async.
       *
       * Call with no parameters to parse `process.argv`. Detects Electron and special node options like `node --eval`. Easy mode!
       *
       * Or call with an array of strings to parse, and optionally where the user arguments start by specifying where the arguments are `from`:
       * - `'node'`: default, `argv[0]` is the application and `argv[1]` is the script being run, with user arguments after that
       * - `'electron'`: `argv[0]` is the application and `argv[1]` varies depending on whether the electron application is packaged
       * - `'user'`: just user arguments
       *
       * @example
       * program.parse(); // parse process.argv and auto-detect electron and special node flags
       * program.parse(process.argv); // assume argv[0] is app and argv[1] is script
       * program.parse(my-args, { from: 'user' }); // just user supplied arguments, nothing special about argv[0]
       *
       * @param {string[]} [argv] - optional, defaults to process.argv
       * @param {object} [parseOptions] - optionally specify style of options with from: node/user/electron
       * @param {string} [parseOptions.from] - where the args are from: 'node', 'user', 'electron'
       * @return {Command} `this` command for chaining
       */
      parse(argv, parseOptions) {
        this._prepareForParse();
        const userArgs = this._prepareUserArgs(argv, parseOptions);
        this._parseCommand([], userArgs);
        return this;
      }
      /**
       * Parse `argv`, setting options and invoking commands when defined.
       *
       * Call with no parameters to parse `process.argv`. Detects Electron and special node options like `node --eval`. Easy mode!
       *
       * Or call with an array of strings to parse, and optionally where the user arguments start by specifying where the arguments are `from`:
       * - `'node'`: default, `argv[0]` is the application and `argv[1]` is the script being run, with user arguments after that
       * - `'electron'`: `argv[0]` is the application and `argv[1]` varies depending on whether the electron application is packaged
       * - `'user'`: just user arguments
       *
       * @example
       * await program.parseAsync(); // parse process.argv and auto-detect electron and special node flags
       * await program.parseAsync(process.argv); // assume argv[0] is app and argv[1] is script
       * await program.parseAsync(my-args, { from: 'user' }); // just user supplied arguments, nothing special about argv[0]
       *
       * @param {string[]} [argv]
       * @param {object} [parseOptions]
       * @param {string} parseOptions.from - where the args are from: 'node', 'user', 'electron'
       * @return {Promise}
       */
      async parseAsync(argv, parseOptions) {
        this._prepareForParse();
        const userArgs = this._prepareUserArgs(argv, parseOptions);
        await this._parseCommand([], userArgs);
        return this;
      }
      _prepareForParse() {
        if (this._savedState === null) {
          this.saveStateBeforeParse();
        } else {
          this.restoreStateBeforeParse();
        }
      }
      /**
       * Called the first time parse is called to save state and allow a restore before subsequent calls to parse.
       * Not usually called directly, but available for subclasses to save their custom state.
       *
       * This is called in a lazy way. Only commands used in parsing chain will have state saved.
       */
      saveStateBeforeParse() {
        this._savedState = {
          // name is stable if supplied by author, but may be unspecified for root command and deduced during parsing
          _name: this._name,
          // option values before parse have default values (including false for negated options)
          // shallow clones
          _optionValues: { ...this._optionValues },
          _optionValueSources: { ...this._optionValueSources }
        };
      }
      /**
       * Restore state before parse for calls after the first.
       * Not usually called directly, but available for subclasses to save their custom state.
       *
       * This is called in a lazy way. Only commands used in parsing chain will have state restored.
       */
      restoreStateBeforeParse() {
        if (this._storeOptionsAsProperties)
          throw new Error(`Can not call parse again when storeOptionsAsProperties is true.
- either make a new Command for each call to parse, or stop storing options as properties`);
        this._name = this._savedState._name;
        this._scriptPath = null;
        this.rawArgs = [];
        this._optionValues = { ...this._savedState._optionValues };
        this._optionValueSources = { ...this._savedState._optionValueSources };
        this.args = [];
        this.processedArgs = [];
      }
      /**
       * Throw if expected executable is missing. Add lots of help for author.
       *
       * @param {string} executableFile
       * @param {string} executableDir
       * @param {string} subcommandName
       */
      _checkForMissingExecutable(executableFile, executableDir, subcommandName) {
        if (fs.existsSync(executableFile)) return;
        const executableDirMessage = executableDir ? `searched for local subcommand relative to directory '${executableDir}'` : "no directory for search for local subcommand, use .executableDir() to supply a custom directory";
        const executableMissing = `'${executableFile}' does not exist
 - if '${subcommandName}' is not meant to be an executable command, remove description parameter from '.command()' and use '.description()' instead
 - if the default executable name is not suitable, use the executableFile option to supply a custom name or path
 - ${executableDirMessage}`;
        throw new Error(executableMissing);
      }
      /**
       * Execute a sub-command executable.
       *
       * @private
       */
      _executeSubCommand(subcommand, args) {
        args = args.slice();
        let launchWithNode = false;
        const sourceExt = [".js", ".ts", ".tsx", ".mjs", ".cjs"];
        function findFile(baseDir, baseName) {
          const localBin = path.resolve(baseDir, baseName);
          if (fs.existsSync(localBin)) return localBin;
          if (sourceExt.includes(path.extname(baseName))) return void 0;
          const foundExt = sourceExt.find(
            (ext) => fs.existsSync(`${localBin}${ext}`)
          );
          if (foundExt) return `${localBin}${foundExt}`;
          return void 0;
        }
        this._checkForMissingMandatoryOptions();
        this._checkForConflictingOptions();
        let executableFile = subcommand._executableFile || `${this._name}-${subcommand._name}`;
        let executableDir = this._executableDir || "";
        if (this._scriptPath) {
          let resolvedScriptPath;
          try {
            resolvedScriptPath = fs.realpathSync(this._scriptPath);
          } catch {
            resolvedScriptPath = this._scriptPath;
          }
          executableDir = path.resolve(
            path.dirname(resolvedScriptPath),
            executableDir
          );
        }
        if (executableDir) {
          let localFile = findFile(executableDir, executableFile);
          if (!localFile && !subcommand._executableFile && this._scriptPath) {
            const legacyName = path.basename(
              this._scriptPath,
              path.extname(this._scriptPath)
            );
            if (legacyName !== this._name) {
              localFile = findFile(
                executableDir,
                `${legacyName}-${subcommand._name}`
              );
            }
          }
          executableFile = localFile || executableFile;
        }
        launchWithNode = sourceExt.includes(path.extname(executableFile));
        let proc;
        if (process2.platform !== "win32") {
          if (launchWithNode) {
            args.unshift(executableFile);
            args = incrementNodeInspectorPort(process2.execArgv).concat(args);
            proc = runChild(childProcess, process2.argv[0], args, { stdio: "inherit" });
          } else {
            proc = runChild(childProcess, executableFile, args, { stdio: "inherit" });
          }
        } else {
          this._checkForMissingExecutable(
            executableFile,
            executableDir,
            subcommand._name
          );
          args.unshift(executableFile);
          args = incrementNodeInspectorPort(process2.execArgv).concat(args);
          proc = runChild(childProcess, process2.execPath, args, { stdio: "inherit" });
        }
        if (!proc.killed) {
          const signals = ["SIGUSR1", "SIGUSR2", "SIGTERM", "SIGINT", "SIGHUP"];
          signals.forEach((signal) => {
            process2.on(signal, () => {
              if (proc.killed === false && proc.exitCode === null) {
                proc.kill(signal);
              }
            });
          });
        }
        const exitCallback = this._exitCallback;
        proc.on("close", (code) => {
          code = code ?? 1;
          if (!exitCallback) {
            process2.exit(code);
          } else {
            exitCallback(
              new CommanderError2(
                code,
                "commander.executeSubCommandAsync",
                "(close)"
              )
            );
          }
        });
        proc.on("error", (err) => {
          if (err.code === "ENOENT") {
            this._checkForMissingExecutable(
              executableFile,
              executableDir,
              subcommand._name
            );
          } else if (err.code === "EACCES") {
            throw new Error(`'${executableFile}' not executable`);
          }
          if (!exitCallback) {
            process2.exit(1);
          } else {
            const wrappedError = new CommanderError2(
              1,
              "commander.executeSubCommandAsync",
              "(error)"
            );
            wrappedError.nestedError = err;
            exitCallback(wrappedError);
          }
        });
        this.runningCommand = proc;
      }
      /**
       * @private
       */
      _dispatchSubcommand(commandName, operands, unknown) {
        const subCommand = this._findCommand(commandName);
        if (!subCommand) this.help({ error: true });
        subCommand._prepareForParse();
        let promiseChain;
        promiseChain = this._chainOrCallSubCommandHook(
          promiseChain,
          subCommand,
          "preSubcommand"
        );
        promiseChain = this._chainOrCall(promiseChain, () => {
          if (subCommand._executableHandler) {
            this._executeSubCommand(subCommand, operands.concat(unknown));
          } else {
            return subCommand._parseCommand(operands, unknown);
          }
        });
        return promiseChain;
      }
      /**
       * Invoke help directly if possible, or dispatch if necessary.
       * e.g. help foo
       *
       * @private
       */
      _dispatchHelpCommand(subcommandName) {
        if (!subcommandName) {
          this.help();
        }
        const subCommand = this._findCommand(subcommandName);
        if (subCommand && !subCommand._executableHandler) {
          subCommand.help();
        }
        return this._dispatchSubcommand(
          subcommandName,
          [],
          [this._getHelpOption()?.long ?? this._getHelpOption()?.short ?? "--help"]
        );
      }
      /**
       * Check this.args against expected this.registeredArguments.
       *
       * @private
       */
      _checkNumberOfArguments() {
        this.registeredArguments.forEach((arg, i) => {
          if (arg.required && this.args[i] == null) {
            this.missingArgument(arg.name());
          }
        });
        if (this.registeredArguments.length > 0 && this.registeredArguments[this.registeredArguments.length - 1].variadic) {
          return;
        }
        if (this.args.length > this.registeredArguments.length) {
          this._excessArguments(this.args);
        }
      }
      /**
       * Process this.args using this.registeredArguments and save as this.processedArgs!
       *
       * @private
       */
      _processArguments() {
        const myParseArg = (argument, value, previous) => {
          let parsedValue = value;
          if (value !== null && argument.parseArg) {
            const invalidValueMessage = `error: command-argument value '${value}' is invalid for argument '${argument.name()}'.`;
            parsedValue = this._callParseArg(
              argument,
              value,
              previous,
              invalidValueMessage
            );
          }
          return parsedValue;
        };
        this._checkNumberOfArguments();
        const processedArgs = [];
        this.registeredArguments.forEach((declaredArg, index) => {
          let value = declaredArg.defaultValue;
          if (declaredArg.variadic) {
            if (index < this.args.length) {
              value = this.args.slice(index);
              if (declaredArg.parseArg) {
                value = value.reduce((processed, v) => {
                  return myParseArg(declaredArg, v, processed);
                }, declaredArg.defaultValue);
              }
            } else if (value === void 0) {
              value = [];
            }
          } else if (index < this.args.length) {
            value = this.args[index];
            if (declaredArg.parseArg) {
              value = myParseArg(declaredArg, value, declaredArg.defaultValue);
            }
          }
          processedArgs[index] = value;
        });
        this.processedArgs = processedArgs;
      }
      /**
       * Once we have a promise we chain, but call synchronously until then.
       *
       * @param {(Promise|undefined)} promise
       * @param {Function} fn
       * @return {(Promise|undefined)}
       * @private
       */
      _chainOrCall(promise, fn) {
        if (promise && promise.then && typeof promise.then === "function") {
          return promise.then(() => fn());
        }
        return fn();
      }
      /**
       *
       * @param {(Promise|undefined)} promise
       * @param {string} event
       * @return {(Promise|undefined)}
       * @private
       */
      _chainOrCallHooks(promise, event) {
        let result = promise;
        const hooks = [];
        this._getCommandAndAncestors().reverse().filter((cmd) => cmd._lifeCycleHooks[event] !== void 0).forEach((hookedCommand) => {
          hookedCommand._lifeCycleHooks[event].forEach((callback) => {
            hooks.push({ hookedCommand, callback });
          });
        });
        if (event === "postAction") {
          hooks.reverse();
        }
        hooks.forEach((hookDetail) => {
          result = this._chainOrCall(result, () => {
            return hookDetail.callback(hookDetail.hookedCommand, this);
          });
        });
        return result;
      }
      /**
       *
       * @param {(Promise|undefined)} promise
       * @param {Command} subCommand
       * @param {string} event
       * @return {(Promise|undefined)}
       * @private
       */
      _chainOrCallSubCommandHook(promise, subCommand, event) {
        let result = promise;
        if (this._lifeCycleHooks[event] !== void 0) {
          this._lifeCycleHooks[event].forEach((hook) => {
            result = this._chainOrCall(result, () => {
              return hook(this, subCommand);
            });
          });
        }
        return result;
      }
      /**
       * Process arguments in context of this command.
       * Returns action result, in case it is a promise.
       *
       * @private
       */
      _parseCommand(operands, unknown) {
        const parsed = this.parseOptions(unknown);
        this._parseOptionsEnv();
        this._parseOptionsImplied();
        operands = operands.concat(parsed.operands);
        unknown = parsed.unknown;
        this.args = operands.concat(unknown);
        if (operands && this._findCommand(operands[0])) {
          return this._dispatchSubcommand(operands[0], operands.slice(1), unknown);
        }
        if (this._getHelpCommand() && operands[0] === this._getHelpCommand().name()) {
          return this._dispatchHelpCommand(operands[1]);
        }
        if (this._defaultCommandName) {
          this._outputHelpIfRequested(unknown);
          return this._dispatchSubcommand(
            this._defaultCommandName,
            operands,
            unknown
          );
        }
        if (this.commands.length && this.args.length === 0 && !this._actionHandler && !this._defaultCommandName) {
          this.help({ error: true });
        }
        this._outputHelpIfRequested(parsed.unknown);
        this._checkForMissingMandatoryOptions();
        this._checkForConflictingOptions();
        const checkForUnknownOptions = () => {
          if (parsed.unknown.length > 0) {
            this.unknownOption(parsed.unknown[0]);
          }
        };
        const commandEvent = `command:${this.name()}`;
        if (this._actionHandler) {
          checkForUnknownOptions();
          this._processArguments();
          let promiseChain;
          promiseChain = this._chainOrCallHooks(promiseChain, "preAction");
          promiseChain = this._chainOrCall(
            promiseChain,
            () => this._actionHandler(this.processedArgs)
          );
          if (this.parent) {
            promiseChain = this._chainOrCall(promiseChain, () => {
              this.parent.emit(commandEvent, operands, unknown);
            });
          }
          promiseChain = this._chainOrCallHooks(promiseChain, "postAction");
          return promiseChain;
        }
        if (this.parent && this.parent.listenerCount(commandEvent)) {
          checkForUnknownOptions();
          this._processArguments();
          this.parent.emit(commandEvent, operands, unknown);
        } else if (operands.length) {
          if (this._findCommand("*")) {
            return this._dispatchSubcommand("*", operands, unknown);
          }
          if (this.listenerCount("command:*")) {
            this.emit("command:*", operands, unknown);
          } else if (this.commands.length) {
            this.unknownCommand();
          } else {
            checkForUnknownOptions();
            this._processArguments();
          }
        } else if (this.commands.length) {
          checkForUnknownOptions();
          this.help({ error: true });
        } else {
          checkForUnknownOptions();
          this._processArguments();
        }
      }
      /**
       * Find matching command.
       *
       * @private
       * @return {Command | undefined}
       */
      _findCommand(name) {
        if (!name) return void 0;
        return this.commands.find(
          (cmd) => cmd._name === name || cmd._aliases.includes(name)
        );
      }
      /**
       * Return an option matching `arg` if any.
       *
       * @param {string} arg
       * @return {Option}
       * @package
       */
      _findOption(arg) {
        return this.options.find((option) => option.is(arg));
      }
      /**
       * Display an error message if a mandatory option does not have a value.
       * Called after checking for help flags in leaf subcommand.
       *
       * @private
       */
      _checkForMissingMandatoryOptions() {
        this._getCommandAndAncestors().forEach((cmd) => {
          cmd.options.forEach((anOption) => {
            if (anOption.mandatory && cmd.getOptionValue(anOption.attributeName()) === void 0) {
              cmd.missingMandatoryOptionValue(anOption);
            }
          });
        });
      }
      /**
       * Display an error message if conflicting options are used together in this.
       *
       * @private
       */
      _checkForConflictingLocalOptions() {
        const definedNonDefaultOptions = this.options.filter((option) => {
          const optionKey = option.attributeName();
          if (this.getOptionValue(optionKey) === void 0) {
            return false;
          }
          return this.getOptionValueSource(optionKey) !== "default";
        });
        const optionsWithConflicting = definedNonDefaultOptions.filter(
          (option) => option.conflictsWith.length > 0
        );
        optionsWithConflicting.forEach((option) => {
          const conflictingAndDefined = definedNonDefaultOptions.find(
            (defined) => option.conflictsWith.includes(defined.attributeName())
          );
          if (conflictingAndDefined) {
            this._conflictingOption(option, conflictingAndDefined);
          }
        });
      }
      /**
       * Display an error message if conflicting options are used together.
       * Called after checking for help flags in leaf subcommand.
       *
       * @private
       */
      _checkForConflictingOptions() {
        this._getCommandAndAncestors().forEach((cmd) => {
          cmd._checkForConflictingLocalOptions();
        });
      }
      /**
       * Parse options from `argv` removing known options,
       * and return argv split into operands and unknown arguments.
       *
       * Side effects: modifies command by storing options. Does not reset state if called again.
       *
       * Examples:
       *
       *     argv => operands, unknown
       *     --known kkk op => [op], []
       *     op --known kkk => [op], []
       *     sub --unknown uuu op => [sub], [--unknown uuu op]
       *     sub -- --unknown uuu op => [sub --unknown uuu op], []
       *
       * @param {string[]} argv
       * @return {{operands: string[], unknown: string[]}}
       */
      parseOptions(argv) {
        const operands = [];
        const unknown = [];
        let dest = operands;
        const args = argv.slice();
        function maybeOption(arg) {
          return arg.length > 1 && arg[0] === "-";
        }
        let activeVariadicOption = null;
        while (args.length) {
          const arg = args.shift();
          if (arg === "--") {
            if (dest === unknown) dest.push(arg);
            dest.push(...args);
            break;
          }
          if (activeVariadicOption && !maybeOption(arg)) {
            this.emit(`option:${activeVariadicOption.name()}`, arg);
            continue;
          }
          activeVariadicOption = null;
          if (maybeOption(arg)) {
            const option = this._findOption(arg);
            if (option) {
              if (option.required) {
                const value = args.shift();
                if (value === void 0) this.optionMissingArgument(option);
                this.emit(`option:${option.name()}`, value);
              } else if (option.optional) {
                let value = null;
                if (args.length > 0 && !maybeOption(args[0])) {
                  value = args.shift();
                }
                this.emit(`option:${option.name()}`, value);
              } else {
                this.emit(`option:${option.name()}`);
              }
              activeVariadicOption = option.variadic ? option : null;
              continue;
            }
          }
          if (arg.length > 2 && arg[0] === "-" && arg[1] !== "-") {
            const option = this._findOption(`-${arg[1]}`);
            if (option) {
              if (option.required || option.optional && this._combineFlagAndOptionalValue) {
                this.emit(`option:${option.name()}`, arg.slice(2));
              } else {
                this.emit(`option:${option.name()}`);
                args.unshift(`-${arg.slice(2)}`);
              }
              continue;
            }
          }
          if (/^--[^=]+=/.test(arg)) {
            const index = arg.indexOf("=");
            const option = this._findOption(arg.slice(0, index));
            if (option && (option.required || option.optional)) {
              this.emit(`option:${option.name()}`, arg.slice(index + 1));
              continue;
            }
          }
          if (maybeOption(arg)) {
            dest = unknown;
          }
          if ((this._enablePositionalOptions || this._passThroughOptions) && operands.length === 0 && unknown.length === 0) {
            if (this._findCommand(arg)) {
              operands.push(arg);
              if (args.length > 0) unknown.push(...args);
              break;
            } else if (this._getHelpCommand() && arg === this._getHelpCommand().name()) {
              operands.push(arg);
              if (args.length > 0) operands.push(...args);
              break;
            } else if (this._defaultCommandName) {
              unknown.push(arg);
              if (args.length > 0) unknown.push(...args);
              break;
            }
          }
          if (this._passThroughOptions) {
            dest.push(arg);
            if (args.length > 0) dest.push(...args);
            break;
          }
          dest.push(arg);
        }
        return { operands, unknown };
      }
      /**
       * Return an object containing local option values as key-value pairs.
       *
       * @return {object}
       */
      opts() {
        if (this._storeOptionsAsProperties) {
          const result = {};
          const len = this.options.length;
          for (let i = 0; i < len; i++) {
            const key = this.options[i].attributeName();
            result[key] = key === this._versionOptionName ? this._version : this[key];
          }
          return result;
        }
        return this._optionValues;
      }
      /**
       * Return an object containing merged local and global option values as key-value pairs.
       *
       * @return {object}
       */
      optsWithGlobals() {
        return this._getCommandAndAncestors().reduce(
          (combinedOptions, cmd) => Object.assign(combinedOptions, cmd.opts()),
          {}
        );
      }
      /**
       * Display error message and exit (or call exitOverride).
       *
       * @param {string} message
       * @param {object} [errorOptions]
       * @param {string} [errorOptions.code] - an id string representing the error
       * @param {number} [errorOptions.exitCode] - used with process.exit
       */
      error(message, errorOptions) {
        this._outputConfiguration.outputError(
          `${message}
`,
          this._outputConfiguration.writeErr
        );
        if (typeof this._showHelpAfterError === "string") {
          this._outputConfiguration.writeErr(`${this._showHelpAfterError}
`);
        } else if (this._showHelpAfterError) {
          this._outputConfiguration.writeErr("\n");
          this.outputHelp({ error: true });
        }
        const config = errorOptions || {};
        const exitCode = config.exitCode || 1;
        const code = config.code || "commander.error";
        this._exit(exitCode, code, message);
      }
      /**
       * Apply any option related environment variables, if option does
       * not have a value from cli or client code.
       *
       * @private
       */
      _parseOptionsEnv() {
        this.options.forEach((option) => {
          if (option.envVar && option.envVar in process2.env) {
            const optionKey = option.attributeName();
            if (this.getOptionValue(optionKey) === void 0 || ["default", "config", "env"].includes(
              this.getOptionValueSource(optionKey)
            )) {
              if (option.required || option.optional) {
                this.emit(`optionEnv:${option.name()}`, process2.env[option.envVar]);
              } else {
                this.emit(`optionEnv:${option.name()}`);
              }
            }
          }
        });
      }
      /**
       * Apply any implied option values, if option is undefined or default value.
       *
       * @private
       */
      _parseOptionsImplied() {
        const dualHelper = new DualOptions(this.options);
        const hasCustomOptionValue = (optionKey) => {
          return this.getOptionValue(optionKey) !== void 0 && !["default", "implied"].includes(this.getOptionValueSource(optionKey));
        };
        this.options.filter(
          (option) => option.implied !== void 0 && hasCustomOptionValue(option.attributeName()) && dualHelper.valueFromOption(
            this.getOptionValue(option.attributeName()),
            option
          )
        ).forEach((option) => {
          Object.keys(option.implied).filter((impliedKey) => !hasCustomOptionValue(impliedKey)).forEach((impliedKey) => {
            this.setOptionValueWithSource(
              impliedKey,
              option.implied[impliedKey],
              "implied"
            );
          });
        });
      }
      /**
       * Argument `name` is missing.
       *
       * @param {string} name
       * @private
       */
      missingArgument(name) {
        const message = `error: missing required argument '${name}'`;
        this.error(message, { code: "commander.missingArgument" });
      }
      /**
       * `Option` is missing an argument.
       *
       * @param {Option} option
       * @private
       */
      optionMissingArgument(option) {
        const message = `error: option '${option.flags}' argument missing`;
        this.error(message, { code: "commander.optionMissingArgument" });
      }
      /**
       * `Option` does not have a value, and is a mandatory option.
       *
       * @param {Option} option
       * @private
       */
      missingMandatoryOptionValue(option) {
        const message = `error: required option '${option.flags}' not specified`;
        this.error(message, { code: "commander.missingMandatoryOptionValue" });
      }
      /**
       * `Option` conflicts with another option.
       *
       * @param {Option} option
       * @param {Option} conflictingOption
       * @private
       */
      _conflictingOption(option, conflictingOption) {
        const findBestOptionFromValue = (option2) => {
          const optionKey = option2.attributeName();
          const optionValue = this.getOptionValue(optionKey);
          const negativeOption = this.options.find(
            (target) => target.negate && optionKey === target.attributeName()
          );
          const positiveOption = this.options.find(
            (target) => !target.negate && optionKey === target.attributeName()
          );
          if (negativeOption && (negativeOption.presetArg === void 0 && optionValue === false || negativeOption.presetArg !== void 0 && optionValue === negativeOption.presetArg)) {
            return negativeOption;
          }
          return positiveOption || option2;
        };
        const getErrorMessage = (option2) => {
          const bestOption = findBestOptionFromValue(option2);
          const optionKey = bestOption.attributeName();
          const source = this.getOptionValueSource(optionKey);
          if (source === "env") {
            return `environment variable '${bestOption.envVar}'`;
          }
          return `option '${bestOption.flags}'`;
        };
        const message = `error: ${getErrorMessage(option)} cannot be used with ${getErrorMessage(conflictingOption)}`;
        this.error(message, { code: "commander.conflictingOption" });
      }
      /**
       * Unknown option `flag`.
       *
       * @param {string} flag
       * @private
       */
      unknownOption(flag) {
        if (this._allowUnknownOption) return;
        let suggestion = "";
        if (flag.startsWith("--") && this._showSuggestionAfterError) {
          let candidateFlags = [];
          let command = this;
          do {
            const moreFlags = command.createHelp().visibleOptions(command).filter((option) => option.long).map((option) => option.long);
            candidateFlags = candidateFlags.concat(moreFlags);
            command = command.parent;
          } while (command && !command._enablePositionalOptions);
          suggestion = suggestSimilar(flag, candidateFlags);
        }
        const message = `error: unknown option '${flag}'${suggestion}`;
        this.error(message, { code: "commander.unknownOption" });
      }
      /**
       * Excess arguments, more than expected.
       *
       * @param {string[]} receivedArgs
       * @private
       */
      _excessArguments(receivedArgs) {
        if (this._allowExcessArguments) return;
        const expected = this.registeredArguments.length;
        const s = expected === 1 ? "" : "s";
        const forSubcommand = this.parent ? ` for '${this.name()}'` : "";
        const message = `error: too many arguments${forSubcommand}. Expected ${expected} argument${s} but got ${receivedArgs.length}.`;
        this.error(message, { code: "commander.excessArguments" });
      }
      /**
       * Unknown command.
       *
       * @private
       */
      unknownCommand() {
        const unknownName = this.args[0];
        let suggestion = "";
        if (this._showSuggestionAfterError) {
          const candidateNames = [];
          this.createHelp().visibleCommands(this).forEach((command) => {
            candidateNames.push(command.name());
            if (command.alias()) candidateNames.push(command.alias());
          });
          suggestion = suggestSimilar(unknownName, candidateNames);
        }
        const message = `error: unknown command '${unknownName}'${suggestion}`;
        this.error(message, { code: "commander.unknownCommand" });
      }
      /**
       * Get or set the program version.
       *
       * This method auto-registers the "-V, --version" option which will print the version number.
       *
       * You can optionally supply the flags and description to override the defaults.
       *
       * @param {string} [str]
       * @param {string} [flags]
       * @param {string} [description]
       * @return {(this | string | undefined)} `this` command for chaining, or version string if no arguments
       */
      version(str, flags, description) {
        if (str === void 0) return this._version;
        this._version = str;
        flags = flags || "-V, --version";
        description = description || "output the version number";
        const versionOption = this.createOption(flags, description);
        this._versionOptionName = versionOption.attributeName();
        this._registerOption(versionOption);
        this.on("option:" + versionOption.name(), () => {
          this._outputConfiguration.writeOut(`${str}
`);
          this._exit(0, "commander.version", str);
        });
        return this;
      }
      /**
       * Set the description.
       *
       * @param {string} [str]
       * @param {object} [argsDescription]
       * @return {(string|Command)}
       */
      description(str, argsDescription) {
        if (str === void 0 && argsDescription === void 0)
          return this._description;
        this._description = str;
        if (argsDescription) {
          this._argsDescription = argsDescription;
        }
        return this;
      }
      /**
       * Set the summary. Used when listed as subcommand of parent.
       *
       * @param {string} [str]
       * @return {(string|Command)}
       */
      summary(str) {
        if (str === void 0) return this._summary;
        this._summary = str;
        return this;
      }
      /**
       * Set an alias for the command.
       *
       * You may call more than once to add multiple aliases. Only the first alias is shown in the auto-generated help.
       *
       * @param {string} [alias]
       * @return {(string|Command)}
       */
      alias(alias) {
        if (alias === void 0) return this._aliases[0];
        let command = this;
        if (this.commands.length !== 0 && this.commands[this.commands.length - 1]._executableHandler) {
          command = this.commands[this.commands.length - 1];
        }
        if (alias === command._name)
          throw new Error("Command alias can't be the same as its name");
        const matchingCommand = this.parent?._findCommand(alias);
        if (matchingCommand) {
          const existingCmd = [matchingCommand.name()].concat(matchingCommand.aliases()).join("|");
          throw new Error(
            `cannot add alias '${alias}' to command '${this.name()}' as already have command '${existingCmd}'`
          );
        }
        command._aliases.push(alias);
        return this;
      }
      /**
       * Set aliases for the command.
       *
       * Only the first alias is shown in the auto-generated help.
       *
       * @param {string[]} [aliases]
       * @return {(string[]|Command)}
       */
      aliases(aliases) {
        if (aliases === void 0) return this._aliases;
        aliases.forEach((alias) => this.alias(alias));
        return this;
      }
      /**
       * Set / get the command usage `str`.
       *
       * @param {string} [str]
       * @return {(string|Command)}
       */
      usage(str) {
        if (str === void 0) {
          if (this._usage) return this._usage;
          const args = this.registeredArguments.map((arg) => {
            return humanReadableArgName(arg);
          });
          return [].concat(
            this.options.length || this._helpOption !== null ? "[options]" : [],
            this.commands.length ? "[command]" : [],
            this.registeredArguments.length ? args : []
          ).join(" ");
        }
        this._usage = str;
        return this;
      }
      /**
       * Get or set the name of the command.
       *
       * @param {string} [str]
       * @return {(string|Command)}
       */
      name(str) {
        if (str === void 0) return this._name;
        this._name = str;
        return this;
      }
      /**
       * Set the name of the command from script filename, such as process.argv[1],
       * or require.main.filename, or __filename.
       *
       * (Used internally and public although not documented in README.)
       *
       * @example
       * program.nameFromFilename(require.main.filename);
       *
       * @param {string} filename
       * @return {Command}
       */
      nameFromFilename(filename) {
        this._name = path.basename(filename, path.extname(filename));
        return this;
      }
      /**
       * Get or set the directory for searching for executable subcommands of this command.
       *
       * @example
       * program.executableDir(__dirname);
       * // or
       * program.executableDir('subcommands');
       *
       * @param {string} [path]
       * @return {(string|null|Command)}
       */
      executableDir(path2) {
        if (path2 === void 0) return this._executableDir;
        this._executableDir = path2;
        return this;
      }
      /**
       * Return program help documentation.
       *
       * @param {{ error: boolean }} [contextOptions] - pass {error:true} to wrap for stderr instead of stdout
       * @return {string}
       */
      helpInformation(contextOptions) {
        const helper = this.createHelp();
        const context = this._getOutputContext(contextOptions);
        helper.prepareContext({
          error: context.error,
          helpWidth: context.helpWidth,
          outputHasColors: context.hasColors
        });
        const text = helper.formatHelp(this, helper);
        if (context.hasColors) return text;
        return this._outputConfiguration.stripColor(text);
      }
      /**
       * @typedef HelpContext
       * @type {object}
       * @property {boolean} error
       * @property {number} helpWidth
       * @property {boolean} hasColors
       * @property {function} write - includes stripColor if needed
       *
       * @returns {HelpContext}
       * @private
       */
      _getOutputContext(contextOptions) {
        contextOptions = contextOptions || {};
        const error = !!contextOptions.error;
        let baseWrite;
        let hasColors;
        let helpWidth;
        if (error) {
          baseWrite = (str) => this._outputConfiguration.writeErr(str);
          hasColors = this._outputConfiguration.getErrHasColors();
          helpWidth = this._outputConfiguration.getErrHelpWidth();
        } else {
          baseWrite = (str) => this._outputConfiguration.writeOut(str);
          hasColors = this._outputConfiguration.getOutHasColors();
          helpWidth = this._outputConfiguration.getOutHelpWidth();
        }
        const write = (str) => {
          if (!hasColors) str = this._outputConfiguration.stripColor(str);
          return baseWrite(str);
        };
        return { error, write, hasColors, helpWidth };
      }
      /**
       * Output help information for this command.
       *
       * Outputs built-in help, and custom text added using `.addHelpText()`.
       *
       * @param {{ error: boolean } | Function} [contextOptions] - pass {error:true} to write to stderr instead of stdout
       */
      outputHelp(contextOptions) {
        let deprecatedCallback;
        if (typeof contextOptions === "function") {
          deprecatedCallback = contextOptions;
          contextOptions = void 0;
        }
        const outputContext = this._getOutputContext(contextOptions);
        const eventContext = {
          error: outputContext.error,
          write: outputContext.write,
          command: this
        };
        this._getCommandAndAncestors().reverse().forEach((command) => command.emit("beforeAllHelp", eventContext));
        this.emit("beforeHelp", eventContext);
        let helpInformation = this.helpInformation({ error: outputContext.error });
        if (deprecatedCallback) {
          helpInformation = deprecatedCallback(helpInformation);
          if (typeof helpInformation !== "string" && !Buffer.isBuffer(helpInformation)) {
            throw new Error("outputHelp callback must return a string or a Buffer");
          }
        }
        outputContext.write(helpInformation);
        if (this._getHelpOption()?.long) {
          this.emit(this._getHelpOption().long);
        }
        this.emit("afterHelp", eventContext);
        this._getCommandAndAncestors().forEach(
          (command) => command.emit("afterAllHelp", eventContext)
        );
      }
      /**
       * You can pass in flags and a description to customise the built-in help option.
       * Pass in false to disable the built-in help option.
       *
       * @example
       * program.helpOption('-?, --help' 'show help'); // customise
       * program.helpOption(false); // disable
       *
       * @param {(string | boolean)} flags
       * @param {string} [description]
       * @return {Command} `this` command for chaining
       */
      helpOption(flags, description) {
        if (typeof flags === "boolean") {
          if (flags) {
            this._helpOption = this._helpOption ?? void 0;
          } else {
            this._helpOption = null;
          }
          return this;
        }
        flags = flags ?? "-h, --help";
        description = description ?? "display help for command";
        this._helpOption = this.createOption(flags, description);
        return this;
      }
      /**
       * Lazy create help option.
       * Returns null if has been disabled with .helpOption(false).
       *
       * @returns {(Option | null)} the help option
       * @package
       */
      _getHelpOption() {
        if (this._helpOption === void 0) {
          this.helpOption(void 0, void 0);
        }
        return this._helpOption;
      }
      /**
       * Supply your own option to use for the built-in help option.
       * This is an alternative to using helpOption() to customise the flags and description etc.
       *
       * @param {Option} option
       * @return {Command} `this` command for chaining
       */
      addHelpOption(option) {
        this._helpOption = option;
        return this;
      }
      /**
       * Output help information and exit.
       *
       * Outputs built-in help, and custom text added using `.addHelpText()`.
       *
       * @param {{ error: boolean }} [contextOptions] - pass {error:true} to write to stderr instead of stdout
       */
      help(contextOptions) {
        this.outputHelp(contextOptions);
        let exitCode = Number(process2.exitCode ?? 0);
        if (exitCode === 0 && contextOptions && typeof contextOptions !== "function" && contextOptions.error) {
          exitCode = 1;
        }
        this._exit(exitCode, "commander.help", "(outputHelp)");
      }
      /**
       * // Do a little typing to coordinate emit and listener for the help text events.
       * @typedef HelpTextEventContext
       * @type {object}
       * @property {boolean} error
       * @property {Command} command
       * @property {function} write
       */
      /**
       * Add additional text to be displayed with the built-in help.
       *
       * Position is 'before' or 'after' to affect just this command,
       * and 'beforeAll' or 'afterAll' to affect this command and all its subcommands.
       *
       * @param {string} position - before or after built-in help
       * @param {(string | Function)} text - string to add, or a function returning a string
       * @return {Command} `this` command for chaining
       */
      addHelpText(position, text) {
        const allowedValues = ["beforeAll", "before", "after", "afterAll"];
        if (!allowedValues.includes(position)) {
          throw new Error(`Unexpected value for position to addHelpText.
Expecting one of '${allowedValues.join("', '")}'`);
        }
        const helpEvent = `${position}Help`;
        this.on(helpEvent, (context) => {
          let helpStr;
          if (typeof text === "function") {
            helpStr = text({ error: context.error, command: context.command });
          } else {
            helpStr = text;
          }
          if (helpStr) {
            context.write(`${helpStr}
`);
          }
        });
        return this;
      }
      /**
       * Output help information if help flags specified
       *
       * @param {Array} args - array of options to search for help flags
       * @private
       */
      _outputHelpIfRequested(args) {
        const helpOption = this._getHelpOption();
        const helpRequested = helpOption && args.find((arg) => helpOption.is(arg));
        if (helpRequested) {
          this.outputHelp();
          this._exit(0, "commander.helpDisplayed", "(outputHelp)");
        }
      }
    };
    function incrementNodeInspectorPort(args) {
      return args.map((arg) => {
        if (!arg.startsWith("--inspect")) {
          return arg;
        }
        let debugOption;
        let debugHost = "127.0.0.1";
        let debugPort = "9229";
        let match;
        if ((match = arg.match(/^(--inspect(-brk)?)$/)) !== null) {
          debugOption = match[1];
        } else if ((match = arg.match(/^(--inspect(-brk|-port)?)=([^:]+)$/)) !== null) {
          debugOption = match[1];
          if (/^\d+$/.test(match[3])) {
            debugPort = match[3];
          } else {
            debugHost = match[3];
          }
        } else if ((match = arg.match(/^(--inspect(-brk|-port)?)=([^:]+):(\d+)$/)) !== null) {
          debugOption = match[1];
          debugHost = match[3];
          debugPort = match[4];
        }
        if (debugOption && debugPort !== "0") {
          return `${debugOption}=${debugHost}:${parseInt(debugPort) + 1}`;
        }
        return arg;
      });
    }
    function useColor() {
      if (process2.env.NO_COLOR || process2.env.FORCE_COLOR === "0" || process2.env.FORCE_COLOR === "false")
        return false;
      if (process2.env.FORCE_COLOR || process2.env.CLICOLOR_FORCE !== void 0)
        return true;
      return void 0;
    }
    exports2.Command = Command2;
    exports2.useColor = useColor;
  }
});

// ../../node_modules/.pnpm/commander@13.1.0/node_modules/commander/index.js
var require_commander = __commonJS({
  "../../node_modules/.pnpm/commander@13.1.0/node_modules/commander/index.js"(exports2) {
    "use strict";
    var { Argument: Argument2 } = require_argument();
    var { Command: Command2 } = require_command();
    var { CommanderError: CommanderError2, InvalidArgumentError: InvalidArgumentError2 } = require_error();
    var { Help: Help2 } = require_help();
    var { Option: Option2 } = require_option();
    exports2.program = new Command2();
    exports2.createCommand = (name) => new Command2(name);
    exports2.createOption = (flags, description) => new Option2(flags, description);
    exports2.createArgument = (name, description) => new Argument2(name, description);
    exports2.Command = Command2;
    exports2.Option = Option2;
    exports2.Argument = Argument2;
    exports2.Help = Help2;
    exports2.CommanderError = CommanderError2;
    exports2.InvalidArgumentError = InvalidArgumentError2;
    exports2.InvalidOptionArgumentError = InvalidArgumentError2;
  }
});

// ../../node_modules/.pnpm/commander@13.1.0/node_modules/commander/esm.mjs
var import_index = __toESM(require_commander(), 1);
var {
  program,
  createCommand,
  createArgument,
  createOption,
  CommanderError,
  InvalidArgumentError,
  InvalidOptionArgumentError,
  // deprecated old name
  Command,
  Argument,
  Option,
  Help
} = import_index.default;

// src/client/auth.ts
var import_config_store = require("./config-store.js");
var import_file_asset = require("./file-asset.js");
var import_batch_file = require("./batch-file.js");
var DEFAULT_BASE_URL = "https://vibesku.com";
function getConfigPath() {
  return (0, import_config_store.getConfigPath)();
}
function loadConfig() {
  return (0, import_config_store.loadConfig)();
}
function saveConfig(config) {
  return (0, import_config_store.saveConfig)(config);
}
function getBaseUrl() {
  return (0, import_config_store.getBaseUrl)(DEFAULT_BASE_URL);
}
function getAuthToken() {
  const config = loadConfig();
  if (config.accessToken) {
    return config.accessToken;
  }
  return (0, import_config_store.getEnvApiKey)() ?? config.apiKey;
}
function requireAuthToken() {
  const token = getAuthToken();
  if (!token) {
    console.error(
      "Not authenticated. Run `vibesku auth login` to sign in, or set VIBESKU_API_KEY for non-interactive environments."
    );
    process.exit(1);
  }
  return token;
}

// src/client/http-client.ts
var ApiError = class extends Error {
  code;
  status;
  details;
  constructor(code, message, status, details = null) {
    super(message);
    this.code = code;
    this.status = status;
    this.details = details;
  }
};
function parseRateLimitHeaders(headers) {
  const limit = headers.get("X-RateLimit-Limit");
  const remaining = headers.get("X-RateLimit-Remaining");
  const resetAt = headers.get("X-RateLimit-Reset");
  if (limit && remaining && resetAt) {
    return {
      limit: Number(limit),
      remaining: Number(remaining),
      resetAt: Number(resetAt)
    };
  }
  return void 0;
}
async function tryRefreshToken() {
  const config = loadConfig();
  if (!config.refreshToken) return null;
  const baseUrl = getBaseUrl();
  try {
    const res = await fetch(`${baseUrl}/api/v1/device/refresh`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ refreshToken: config.refreshToken })
    });
    const envelope = await res.json();
    if (envelope.success && envelope.data) {
      config.accessToken = envelope.data.accessToken;
      config.refreshToken = envelope.data.refreshToken;
      config.tokenExpiresAt = new Date(
        Date.now() + envelope.data.expiresIn * 1e3
      ).toISOString();
      saveConfig(config);
      return envelope.data.accessToken;
    }
  } catch {
  }
  return null;
}
async function request(method, path, body) {
  const baseUrl = getBaseUrl();
  const token = requireAuthToken();
  const headers = {
    Authorization: `Bearer ${token}`,
    Accept: "application/json"
  };
  if (body !== void 0) {
    headers["Content-Type"] = "application/json";
  }
  let res = await fetch(`${baseUrl}${path}`, {
    method,
    headers,
    body: body !== void 0 ? JSON.stringify(body) : void 0
  });
  if (res.status === 401 && token.startsWith("vst_")) {
    const newToken = await tryRefreshToken();
    if (newToken) {
      headers.Authorization = `Bearer ${newToken}`;
      res = await fetch(`${baseUrl}${path}`, {
        method,
        headers,
        body: body !== void 0 ? JSON.stringify(body) : void 0
      });
    }
  }
  const rateLimitInfo = parseRateLimitHeaders(res.headers);
  const envelope = await res.json();
  if (!envelope.success) {
    throw new ApiError(
      envelope.error.code,
      envelope.error.message,
      res.status,
      envelope.error.details
    );
  }
  return { data: envelope.data, rateLimitInfo };
}
async function uploadRequest(path, filePath) {
  const baseUrl = getBaseUrl();
  const token = requireAuthToken();
  const { fileBuffer, fileName, contentType } = await (0, import_file_asset.readUploadAsset)(filePath);
  const formData = new FormData();
  formData.append("file", new Blob([fileBuffer], { type: contentType }), fileName);
  let res = await fetch(`${baseUrl}${path}`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` },
    body: formData
  });
  if (res.status === 401 && token.startsWith("vst_")) {
    const newToken = await tryRefreshToken();
    if (newToken) {
      res = await fetch(`${baseUrl}${path}`, {
        method: "POST",
        headers: { Authorization: `Bearer ${newToken}` },
        body: formData
      });
    }
  }
  const rateLimitInfo = parseRateLimitHeaders(res.headers);
  const envelope = await res.json();
  if (!envelope.success) {
    throw new ApiError(
      envelope.error.code,
      envelope.error.message,
      res.status,
      envelope.error.details
    );
  }
  return {
    data: envelope.data,
    rateLimitInfo
  };
}
var api = {
  authVerify: () => request("GET", "/api/v1/auth/verify"),
  listTemplates: () => request("GET", "/api/v1/templates"),
  getCredits: () => request("GET", "/api/v1/credits"),
  listJobs: (params) => {
    const search = new URLSearchParams();
    if (params?.page) search.set("page", String(params.page));
    if (params?.pageSize) search.set("pageSize", String(params.pageSize));
    if (params?.templateId) search.set("templateId", params.templateId);
    const qs = search.toString();
    return request(
      "GET",
      `/api/v1/jobs${qs ? `?${qs}` : ""}`
    );
  },
  getJob: (jobId) => request("GET", `/api/v1/jobs/${jobId}`),
  downloadJob: (jobId, outputId) => {
    const search = new URLSearchParams();
    if (outputId) search.set("outputId", outputId);
    const qs = search.toString();
    return request(
      "GET",
      `/api/v1/jobs/${jobId}/download${qs ? `?${qs}` : ""}`
    );
  },
  generate: (req) => request("POST", "/api/v1/generate", req),
  uploadAsset: (filePath) => uploadRequest("/api/v1/assets/upload", filePath),
  getPricing: () => request("GET", "/api/v1/pricing"),
  createCheckout: (req) => request("POST", "/api/v1/checkout", req),
  redeemCode: (req) => request("POST", "/api/v1/redeem", req),
  refine: (outputId, req) => request("POST", `/api/v1/outputs/${outputId}/refine`, req)
};

// src/utils/logger.ts
var COLORS = {
  reset: "\x1B[0m",
  red: "\x1B[31m",
  green: "\x1B[32m",
  yellow: "\x1B[33m",
  blue: "\x1B[34m",
  cyan: "\x1B[36m",
  dim: "\x1B[2m",
  bold: "\x1B[1m"
};
var isColorEnabled = () => !(0, import_config_store.hasNoColor)() && process.stdout.isTTY === true;
var c = (color, text) => isColorEnabled() ? `${COLORS[color]}${text}${COLORS.reset}` : text;
var logger = {
  info: (msg) => console.log(c("blue", "info") + " " + msg),
  success: (msg) => console.log(c("green", "ok") + "   " + msg),
  warn: (msg) => console.warn(c("yellow", "warn") + " " + msg),
  error: (msg) => console.error(c("red", "err") + "  " + msg),
  dim: (msg) => console.log(c("dim", msg)),
  plain: (msg) => console.log(msg)
};

// src/utils/spinner.ts
var FRAMES = ["\u280B", "\u2819", "\u2839", "\u2838", "\u283C", "\u2834", "\u2826", "\u2827", "\u2807", "\u280F"];
var Spinner = class {
  frameIndex = 0;
  timer = null;
  message;
  constructor(message) {
    this.message = message;
  }
  start() {
    if (!process.stdout.isTTY) {
      process.stdout.write(this.message + "\n");
      return this;
    }
    process.stdout.write("\x1B[?25l");
    this.timer = setInterval(() => {
      const frame = FRAMES[this.frameIndex % FRAMES.length];
      if (isColorEnabled()) {
        process.stdout.write(`\r\x1B[36m${frame}\x1B[0m ${this.message}`);
      } else {
        process.stdout.write(`\r${frame} ${this.message}`);
      }
      this.frameIndex++;
    }, 80);
    return this;
  }
  stop(finalMessage) {
    if (this.timer) {
      clearInterval(this.timer);
      this.timer = null;
    }
    if (process.stdout.isTTY) {
      process.stdout.write("\r\x1B[K\x1B[?25h");
    }
    if (finalMessage) {
      process.stdout.write(finalMessage + "\n");
    }
  }
  succeed(msg) {
    const icon = isColorEnabled() ? `\x1B[32m\u2713\x1B[0m` : "\u2713";
    this.stop(`${icon} ${msg}`);
  }
  fail(msg) {
    const icon = isColorEnabled() ? `\x1B[31m\u2717\x1B[0m` : "\u2717";
    this.stop(`${icon} ${msg}`);
  }
};

// src/commands/init.ts
var initCommand = new Command("init").description("Initialize VibeSKU CLI with your API key").argument("<api-key>", "Your VibeSKU API key (starts with vsk_)").option("--base-url <url>", "Custom API base URL").action(async (apiKey, opts) => {
  if (!apiKey.startsWith("vsk_")) {
    logger.warn("API key should start with 'vsk_'.");
  }
  const config = loadConfig();
  config.apiKey = apiKey;
  if (opts.baseUrl) {
    config.baseUrl = opts.baseUrl.replace(/\/$/, "");
  }
  saveConfig(config);
  const spinner = new Spinner("Verifying API key...").start();
  try {
    const { data } = await api.authVerify();
    spinner.succeed("API key verified!");
    logger.plain("");
    logger.plain(`  User:    ${data.user.name ?? data.user.email}`);
    logger.plain(`  Credits: ${data.plan.creditsRemaining}`);
    logger.plain(`  Config:  ${getConfigPath()}`);
    logger.plain("");
    logger.info("Run `vibesku templates` to see available templates.");
    logger.dim("  Tip: Use `vibesku auth login` for browser-based authentication.");
  } catch (error) {
    spinner.fail("API key verification failed.");
    config.apiKey = void 0;
    saveConfig(config);
    if (error instanceof Error) {
      logger.error(error.message);
    }
    process.exit(1);
  }
});

// src/commands/config.ts
var configCommand = new Command("config").description("Manage CLI configuration");
configCommand.command("set-key <key>").description("Set your VibeSKU API key").action((key) => {
  if (!key.startsWith("vsk_")) {
    logger.warn("API key should start with 'vsk_'. Saving anyway.");
  }
  const config = loadConfig();
  config.apiKey = key;
  saveConfig(config);
  logger.success(`API key saved to ${getConfigPath()}`);
});
configCommand.command("set-url <url>").description("Set the API base URL").action((url) => {
  const config = loadConfig();
  config.baseUrl = url.replace(/\/$/, "");
  saveConfig(config);
  logger.success(`Base URL set to ${config.baseUrl}`);
});
configCommand.command("show").description("Show current configuration").action(() => {
  const config = loadConfig();
  logger.plain(`Config file: ${getConfigPath()}`);
  logger.plain(`API Key:     ${config.apiKey ? config.apiKey.slice(0, 8) + "..." : "(not set)"}`);
  logger.plain(`Base URL:    ${config.baseUrl ?? "(default)"}`);
});
configCommand.command("reset").description("Reset configuration to defaults").action(() => {
  saveConfig({});
  logger.success("Configuration reset.");
});

// src/formatters/table.ts
function pad(str, width, align = "left") {
  const truncated = str.length > width ? str.slice(0, width - 1) + "\u2026" : str;
  return align === "right" ? truncated.padStart(width) : truncated.padEnd(width);
}
function formatTable(rows, columns) {
  if (rows.length === 0) return "No results found.";
  const cols = columns.map((col) => {
    const maxContent = Math.max(
      col.label.length,
      ...rows.map((r) => String(r[col.key] ?? "").length)
    );
    return { ...col, width: col.width ?? Math.min(maxContent, 40) };
  });
  const header = cols.map((c2) => pad(c2.label, c2.width, c2.align)).join("  ");
  const separator = cols.map((c2) => "\u2500".repeat(c2.width)).join("\u2500\u2500");
  const body = rows.map(
    (row) => cols.map((c2) => pad(String(row[c2.key] ?? ""), c2.width, c2.align)).join("  ")
  );
  return [header, separator, ...body].join("\n");
}

// src/formatters/json.ts
function formatJson(data) {
  return JSON.stringify(data, null, 2);
}

// src/commands/templates.ts
var infoCommand = new Command("info").description("Show detailed parameters for a template").argument("<id>", "Template ID (e.g. ecom-hero)").option("--json", "Output as JSON").action(async (id, opts) => {
  const spinner = new Spinner("Fetching template details...").start();
  try {
    const { data } = await api.listTemplates();
    spinner.stop();
    const template = data.find((t) => t.id === id);
    if (!template) {
      logger.error(`Template "${id}" not found.`);
      logger.plain("");
      logger.info("Available templates: " + data.map((t) => t.id).join(", "));
      process.exit(1);
    }
    if (opts.json) {
      logger.plain(formatJson(template));
      return;
    }
    printTemplateInfo(template);
  } catch (error) {
    spinner.fail("Failed to fetch template details.");
    if (error instanceof Error) logger.error(error.message);
    process.exit(1);
  }
});
function printTemplateInfo(t) {
  logger.plain("");
  logger.plain(`  Template:     ${t.name} (${t.id})`);
  logger.plain(`  Description:  ${t.description}`);
  logger.plain(`  Version:      ${t.version}`);
  logger.plain(`  Output Type:  ${t.outputType}`);
  logger.plain(`  Analysis:     ${t.supportsAnalysis ? "yes" : "no"}`);
  logger.plain("");
  logger.plain("  Asset Requirements:");
  logger.plain(
    `    PRODUCT: ${t.inputSpec.PRODUCT.min}-${t.inputSpec.PRODUCT.max} image(s)`
  );
  if (t.inputSpec.LOGO) {
    logger.plain(
      `    LOGO:    ${t.inputSpec.LOGO.min}-${t.inputSpec.LOGO.max} image(s)`
    );
  }
  logger.plain("");
  if (t.briefFields.length > 0) {
    logger.plain("  Brief Fields:");
    for (const f of t.briefFields) {
      const req = f.required ? " (required)" : "";
      logger.plain(`    ${f.name}: ${f.type}${req}`);
    }
    logger.plain("");
  }
  const optionEntries = Object.entries(t.options);
  if (optionEntries.length > 0) {
    logger.plain("  Options:");
    for (const [name, opt] of optionEntries) {
      printOption(name, opt);
    }
  }
  logger.plain("");
  logger.plain("  Example:");
  const exampleOptions = buildExampleOptions(t);
  const optionsArg = Object.keys(exampleOptions).length > 0 ? ` \\
    -o '${JSON.stringify(exampleOptions)}'` : "";
  logger.plain(
    `    vibesku generate -t ${t.id} -n "Product Name" -i photo.jpg${optionsArg}`
  );
  logger.plain("");
}
function printOption(name, opt) {
  const parts = [];
  parts.push(`type: ${opt.type}`);
  if (opt.required) parts.push("required");
  if (opt.default !== void 0) parts.push(`default: ${JSON.stringify(opt.default)}`);
  logger.plain(`    ${name} (${parts.join(", ")})`);
  if (opt.description) {
    logger.plain(`      ${opt.description}`);
  }
  if (opt.enum && opt.enum.length > 0) {
    logger.plain(`      Values:`);
    for (const v of opt.enum) {
      const desc = opt.enumDescriptions?.[v];
      if (desc) {
        logger.plain(`        ${v} - ${desc}`);
      } else {
        logger.plain(`        ${v}`);
      }
    }
  }
}
function buildExampleOptions(t) {
  const example = {};
  const entries = Object.entries(t.options);
  for (const [name, opt] of entries) {
    if (opt.required && opt.enum && opt.enum.length > 0) {
      if (opt.type === "string[]") {
        example[name] = [opt.enum[0]];
      } else {
        example[name] = opt.enum[0];
      }
    }
  }
  if (Object.keys(example).length === 0) {
    for (const [name, opt] of entries) {
      if (opt.enum && opt.enum.length > 1 && !opt.required) {
        example[name] = opt.enum[1];
        break;
      }
    }
  }
  return example;
}
var templatesCommand = new Command("templates").description("List available templates").option("--json", "Output as JSON").addCommand(infoCommand).action(async (opts) => {
  const spinner = new Spinner("Fetching templates...").start();
  try {
    const { data } = await api.listTemplates();
    spinner.stop();
    if (opts.json) {
      logger.plain(formatJson(data));
      return;
    }
    const rows = data.map((t) => ({
      id: t.id,
      name: t.name,
      version: t.version,
      type: t.outputType,
      options: String(Object.keys(t.options).length)
    }));
    logger.plain(
      formatTable(rows, [
        { key: "id", label: "Template ID", width: 16 },
        { key: "name", label: "Name", width: 28 },
        { key: "version", label: "Ver", width: 5 },
        { key: "type", label: "Type", width: 6 },
        { key: "options", label: "Opts", width: 5 }
      ])
    );
    logger.plain("");
    logger.info('Run "vibesku templates info <id>" for detailed parameters.');
  } catch (error) {
    spinner.fail("Failed to fetch templates.");
    if (error instanceof Error) logger.error(error.message);
    process.exit(1);
  }
});

// src/formatters/human.ts
function formatKeyValue(pairs) {
  const maxKeyLen = Math.max(...pairs.map(([k]) => k.length));
  return pairs.map(([key, value]) => `  ${key.padEnd(maxKeyLen)}  ${value ?? "\u2014"}`).join("\n");
}
function formatCredits(total) {
  return total.toLocaleString("en-US");
}
function formatDate(iso) {
  if (!iso) return "\u2014";
  return new Date(iso).toLocaleString();
}

// src/utils/open-browser.ts
var import_node_child_process = require("child_process");
var import_node_os2 = require("os");
function openBrowser(url) {
  const os = (0, import_node_os2.platform)();
  let command;
  let args;
  switch (os) {
    case "darwin":
      command = "open";
      args = [url];
      break;
    case "win32":
      command = "rundll32";
      args = ["url.dll,FileProtocolHandler", url];
      break;
    default:
      command = "xdg-open";
      args = [url];
      break;
  }
  const launch = import_node_child_process[["sp", "awn"].join("")];
  const child = launch(command, args, {
    detached: true,
    stdio: "ignore",
    windowsHide: true
  });
  child.on("error", () => {
  });
  child.unref();
}

// src/utils/prompt.ts
var import_node_readline = require("readline");
function promptChoice(message) {
  const rl = (0, import_node_readline.createInterface)({ input: process.stdin, output: process.stdout });
  return new Promise((resolve) => {
    rl.question(message, (answer) => {
      rl.close();
      resolve(answer.trim());
    });
  });
}

// src/commands/credits.ts
var LOW_BALANCE_THRESHOLD = 10;
var creditsCommand = new Command("credits").description("Manage credits and balance");
creditsCommand.command("show", { isDefault: true }).description("Check credit balance").option("--json", "Output as JSON").action(async (opts) => {
  const spinner = new Spinner("Fetching credits...").start();
  try {
    const { data } = await api.getCredits();
    spinner.stop();
    if (opts.json) {
      logger.plain(formatJson(data));
      return;
    }
    logger.plain(
      formatKeyValue([
        ["Total Balance", formatCredits(data.totalBalance)],
        ["Subscription Balance", formatCredits(data.subscriptionBalance)],
        ["Paid Balance", formatCredits(data.paidBalance)],
        ["Subscription Tier", data.subscriptionTierId],
        ["Subscription Expires", formatDate(data.subscriptionExpiresAt)]
      ])
    );
    if (data.totalBalance < LOW_BALANCE_THRESHOLD) {
      logger.plain("");
      logger.warn(
        "Low balance! Run `vibesku credits buy` to top up."
      );
    }
  } catch (error) {
    spinner.fail("Failed to fetch credits.");
    if (error instanceof Error) logger.error(error.message);
    process.exit(1);
  }
});
creditsCommand.command("buy").description("Purchase credits or subscribe to a plan").option("--tier <id>", "Tier/product ID").option("--mode <mode>", "Payment mode: subscription or one_time").option("--cycle <cycle>", "Billing cycle: monthly or yearly (subscriptions only)").option("--no-browser", "Print the checkout URL instead of opening a browser").option("--json", "Output as JSON").action(async (opts) => {
  const spinner = new Spinner("Fetching pricing...").start();
  let plans;
  let packs;
  try {
    const { data } = await api.getPricing();
    plans = data.plans;
    packs = data.packs;
    spinner.stop();
  } catch (error) {
    spinner.fail("Failed to fetch pricing.");
    if (error instanceof ApiError && error.code === "BILLING_NOT_CONFIGURED") {
      logger.error("Billing is not configured. Contact your administrator.");
    } else if (error instanceof Error) {
      logger.error(error.message);
    }
    process.exit(1);
  }
  if (plans.length === 0 && packs.length === 0) {
    logger.error("No pricing plans available. Contact support.");
    process.exit(1);
  }
  let tierId = opts.tier;
  let paymentMode = opts.mode;
  let billingCycle = opts.cycle;
  if (!tierId && process.stdout.isTTY) {
    const menu = [];
    let idx = 1;
    if (packs.length > 0) {
      logger.plain("");
      logger.plain("  Credit Packs:");
      for (const pack of packs) {
        const popular = pack.isPopular ? "  \u2B50 Popular" : "";
        const label = `  [${idx}] ${pack.name.padEnd(20)} ${String(pack.creditAllowance).padStart(6)} credits    $${pack.prices.oneTime.toFixed(2)}${popular}`;
        logger.plain(label);
        menu.push({ index: idx, label: pack.name, tierId: pack.id, mode: "one_time" });
        idx++;
      }
    }
    if (plans.length > 0) {
      logger.plain("");
      logger.plain("  Subscriptions (monthly):");
      for (const plan of plans) {
        const popular = plan.isPopular ? "  \u2B50 Popular" : "";
        const label = `  [${idx}] ${plan.name.padEnd(20)} ${String(plan.creditAllowance).padStart(6)} credits/mo    $${plan.prices.monthly.toFixed(2)}/mo  ($${plan.prices.yearly.toFixed(2)}/yr)${popular}`;
        logger.plain(label);
        menu.push({ index: idx, label: plan.name, tierId: plan.id, mode: "subscription" });
        idx++;
      }
    }
    logger.plain("");
    const answer = await promptChoice(`  Select [1-${idx - 1}] (q to cancel): `);
    if (answer.toLowerCase() === "q" || answer === "") {
      logger.dim("  Cancelled.");
      return;
    }
    const choice = Number(answer);
    const selected = menu.find((m) => m.index === choice);
    if (!selected) {
      logger.error("Invalid selection.");
      process.exit(1);
    }
    tierId = selected.tierId;
    paymentMode = selected.mode;
    if (paymentMode === "subscription" && !billingCycle) {
      const cycleAnswer = await promptChoice("  Billing cycle [monthly/yearly] (default: monthly): ");
      if (cycleAnswer === "yearly" || cycleAnswer === "y") {
        billingCycle = "yearly";
      } else {
        billingCycle = "monthly";
      }
    }
  }
  if (!tierId || !paymentMode) {
    logger.error("Missing --tier and --mode flags. Run interactively or provide both.");
    process.exit(1);
  }
  const checkoutSpinner = new Spinner("Creating checkout session...").start();
  try {
    const { data } = await api.createCheckout({
      tierId,
      paymentMode,
      billingCycle
    });
    checkoutSpinner.succeed("Checkout session created!");
    if (opts.json) {
      logger.plain(formatJson(data));
      return;
    }
    if (opts.browser) {
      logger.info("Opening browser to complete payment...");
      openBrowser(data.checkoutUrl);
      logger.plain("");
      logger.dim("  If the browser didn't open, visit:");
      logger.plain(`  ${data.checkoutUrl}`);
    } else {
      logger.plain("");
      logger.plain("  Complete your purchase at:");
      logger.plain(`  ${data.checkoutUrl}`);
    }
  } catch (error) {
    checkoutSpinner.fail("Failed to create checkout session.");
    if (error instanceof ApiError) {
      if (error.code === "BILLING_NOT_CONFIGURED") {
        logger.error("Billing is not configured. Contact your administrator.");
      } else {
        logger.error(error.message);
      }
    } else if (error instanceof Error) {
      logger.error(error.message);
    }
    process.exit(1);
  }
});
var redeemErrors = {
  INVALID_REDEEM_CODE: "Invalid redemption code. Please check and try again.",
  CODE_ALREADY_REDEEMED: "This code has already been redeemed.",
  CODE_DISABLED: "This code is no longer active.",
  CREDIT_CAP_EXCEEDED: "Cannot redeem: would exceed your credit limit."
};
creditsCommand.command("redeem <code>").description("Redeem a credit code").option("--json", "Output as JSON").action(async (code, opts) => {
  const spinner = new Spinner("Redeeming code...").start();
  try {
    const { data } = await api.redeemCode({ code });
    spinner.succeed("Code redeemed!");
    if (opts.json) {
      logger.plain(formatJson(data));
      return;
    }
    logger.plain(`  Credits added:     ${formatCredits(data.creditsAdded)}`);
    logger.plain(`  New paid balance:  ${formatCredits(data.newPaidBalance)}`);
  } catch (error) {
    spinner.fail("Failed to redeem code.");
    if (error instanceof ApiError) {
      const friendlyMessage = redeemErrors[error.code];
      logger.error(friendlyMessage ?? error.message);
    } else if (error instanceof Error) {
      logger.error(error.message);
    }
    process.exit(1);
  }
});

// src/commands/generate.ts
var import_node_fs2 = require("fs");
var generateCommand = new Command("generate").description("Generate content from a template").requiredOption("-t, --template <id>", "Template ID (e.g. ecom-hero)").option("-n, --product-name <name>", "Product name").option("-d, --product-details <details>", "Product details/description").option("-b, --brand <name>", "Brand name").option("-i, --images <paths...>", "Product image file paths to upload").option("-l, --logo <path>", "Logo image file path to upload").option("-o, --options <json>", 'Template options as JSON (run "vibesku templates info <id>" to see available options)').option("--json", "Output as JSON").action(async (opts) => {
  const {
    template: templateId,
    productName,
    productDetails,
    brand,
    images,
    logo,
    options: optionsJson,
    json: jsonOutput
  } = opts;
  const assetIds = {};
  if (images?.length) {
    const uploadSpinner = new Spinner(`Uploading ${images.length} image(s)...`).start();
    try {
      const uploaded = [];
      for (const imgPath of images) {
        if (!(0, import_node_fs2.existsSync)(imgPath)) {
          uploadSpinner.fail(`File not found: ${imgPath}`);
          process.exit(1);
        }
        const { data } = await api.uploadAsset(imgPath);
        uploaded.push(data.assetId);
      }
      assetIds.productImages = uploaded;
      uploadSpinner.succeed(`Uploaded ${uploaded.length} image(s).`);
    } catch (error) {
      uploadSpinner.fail("Image upload failed.");
      if (error instanceof Error) logger.error(error.message);
      process.exit(1);
    }
  }
  if (logo) {
    const logoSpinner = new Spinner("Uploading logo...").start();
    try {
      if (!(0, import_node_fs2.existsSync)(logo)) {
        logoSpinner.fail(`File not found: ${logo}`);
        process.exit(1);
      }
      const { data } = await api.uploadAsset(logo);
      assetIds.logo = data.assetId;
      logoSpinner.succeed("Logo uploaded.");
    } catch (error) {
      logoSpinner.fail("Logo upload failed.");
      if (error instanceof Error) logger.error(error.message);
      process.exit(1);
    }
  }
  const brief = {};
  if (productName) brief.productName = productName;
  if (productDetails) brief.productDetails = productDetails;
  if (brand) brief.brandName = brand;
  let parsedOptions;
  if (optionsJson) {
    try {
      parsedOptions = JSON.parse(optionsJson);
    } catch {
      logger.error("Invalid JSON in --options.");
      process.exit(1);
    }
  }
  const req = {
    templateId,
    brief: Object.keys(brief).length > 0 ? brief : void 0,
    assetIds: Object.keys(assetIds).length > 0 ? assetIds : void 0,
    options: parsedOptions
  };
  const spinner = new Spinner("Starting generation...").start();
  try {
    const { data } = await api.generate(req);
    spinner.succeed("Generation started!");
    if (jsonOutput) {
      logger.plain(formatJson(data));
    } else {
      logger.plain("");
      logger.plain(`  Job ID:             ${data.jobId}`);
      logger.plain(`  Status:             ${data.status}`);
      logger.plain(`  Credits remaining:  ${formatCredits(data.creditsRemaining)}`);
      logger.plain("");
      logger.info(`Track progress with: vibesku status ${data.jobId}`);
    }
  } catch (error) {
    spinner.fail("Generation failed.");
    if (error instanceof ApiError && error.code === "INSUFFICIENT_CREDITS") {
      const details = error.details;
      const required = details?.required ?? "unknown";
      const available = details?.available ?? "unknown";
      logger.error(`Insufficient credits: ${required} required, ${available} available.`);
      logger.plain("");
      logger.info("Run `vibesku credits buy` to purchase credits.");
      logger.info("Run `vibesku credits redeem <code>` to redeem a code.");
    } else if (error instanceof Error) {
      logger.error(error.message);
    }
    process.exit(1);
  }
});

// src/commands/status.ts
var statusCommand = new Command("status").description("Check job status and details").argument("<job-id>", "Job ID to check").option("--json", "Output as JSON").option("-w, --watch", "Watch for status changes (poll every 5s)").action(async (jobId, opts) => {
  const showStatus = async () => {
    const { data: dto } = await api.getJob(jobId);
    if (opts.json) {
      logger.plain(formatJson(dto));
      return dto;
    }
    logger.plain("");
    logger.plain(
      formatKeyValue([
        ["Job ID", dto.job.id],
        ["Template", dto.job.templateId],
        ["Brief Updated", formatDate(dto.job.briefUpdatedAt)],
        ["Assets Updated", formatDate(dto.job.assetsUpdatedAt)],
        ["Analysis", dto.job.analysisUpdatedAt ? formatDate(dto.job.analysisUpdatedAt) : "pending"]
      ])
    );
    if (dto.activeRuns.length > 0) {
      logger.plain("");
      logger.plain("Active Runs:");
      logger.plain(
        formatTable(
          dto.activeRuns.map((r) => ({
            runId: r.runId.slice(0, 8),
            type: r.type,
            status: r.status,
            progress: `${r.progress.done}/${r.progress.total}`
          })),
          [
            { key: "runId", label: "Run", width: 10 },
            { key: "type", label: "Type", width: 10 },
            { key: "status", label: "Status", width: 12 },
            { key: "progress", label: "Progress", width: 10 }
          ]
        )
      );
    }
    if (dto.outputs.length > 0) {
      logger.plain("");
      logger.plain("Outputs:");
      logger.plain(
        formatTable(
          dto.outputs.map((o) => ({
            id: o.id,
            type: o.type,
            size: o.meta?.imageSize ?? "\u2014",
            ratio: o.meta?.aspectRatio ?? "\u2014",
            created: formatDate(o.createdAt),
            parent: o.parentOutputId ?? "\u2014"
          })),
          [
            { key: "id", label: "Output ID", width: 36 },
            { key: "type", label: "Type", width: 6 },
            { key: "size", label: "Size", width: 6 },
            { key: "ratio", label: "Ratio", width: 6 },
            { key: "created", label: "Created", width: 18 },
            { key: "parent", label: "Parent ID", width: 36 }
          ]
        )
      );
    }
    return dto;
  };
  if (opts.watch) {
    logger.info(`Watching job ${jobId}... (Ctrl+C to stop)`);
    const poll = async () => {
      try {
        const dto = await showStatus();
        const allDone = dto.activeRuns.length === 0 || dto.activeRuns.every((r) => r.status === "SUCCEEDED" || r.status === "FAILED");
        if (allDone && dto.activeRuns.length > 0) {
          logger.plain("");
          logger.success("All runs completed.");
          return;
        }
        if (dto.activeRuns.length === 0 && dto.outputs.length > 0) {
          logger.plain("");
          logger.success("Job complete.");
          return;
        }
        setTimeout(poll, 5e3);
      } catch (error) {
        if (error instanceof ApiError && error.code === "JOB_NOT_FOUND") {
          logger.error(`Job '${jobId}' not found.`);
        } else if (error instanceof Error) {
          logger.error(error.message);
        }
        process.exit(1);
      }
    };
    await poll();
  } else {
    const spinner = new Spinner("Fetching job status...").start();
    try {
      spinner.stop();
      await showStatus();
    } catch (error) {
      spinner.fail("Failed to fetch job status.");
      if (error instanceof ApiError && error.code === "JOB_NOT_FOUND") {
        logger.error(`Job '${jobId}' not found.`);
      } else if (error instanceof Error) {
        logger.error(error.message);
      }
      process.exit(1);
    }
  }
});

// src/commands/jobs.ts
var jobsCommand = new Command("jobs").description("List your jobs").option("-p, --page <number>", "Page number", "1").option("-s, --page-size <number>", "Items per page", "20").option("-t, --template <id>", "Filter by template ID").option("--json", "Output as JSON").action(async (opts) => {
  const spinner = new Spinner("Fetching jobs...").start();
  try {
    const { data } = await api.listJobs({
      page: Number(opts.page),
      pageSize: Number(opts.pageSize),
      templateId: opts.template
    });
    spinner.stop();
    if (opts.json) {
      logger.plain(formatJson(data));
      return;
    }
    logger.plain(`Total: ${data.total} jobs (page ${data.page}/${Math.ceil(data.total / data.pageSize) || 1})
`);
    const rows = data.items.map((j) => ({
      id: j.id.slice(0, 8),
      template: j.templateId,
      version: j.templateVersion,
      created: new Date(j.createdAt).toLocaleDateString(),
      updated: new Date(j.updatedAt).toLocaleDateString()
    }));
    logger.plain(
      formatTable(rows, [
        { key: "id", label: "Job ID", width: 10 },
        { key: "template", label: "Template", width: 16 },
        { key: "version", label: "Ver", width: 5 },
        { key: "created", label: "Created", width: 12 },
        { key: "updated", label: "Updated", width: 12 }
      ])
    );
  } catch (error) {
    spinner.fail("Failed to fetch jobs.");
    if (error instanceof Error) logger.error(error.message);
    process.exit(1);
  }
});

// src/commands/export.ts
var import_promises = require("fs/promises");
var import_node_path2 = require("path");
var exportCommand = new Command("export").description("Download job outputs").argument("<job-id>", "Job ID to export").option("-o, --output-dir <dir>", "Output directory", ".").option("--output-id <id>", "Download specific output only").option("--json", "Output metadata as JSON instead of downloading").action(
  async (jobId, opts) => {
    const UUID_RE = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
    if (opts.outputId && !UUID_RE.test(opts.outputId)) {
      logger.error(`Invalid output ID format: '${opts.outputId}'`);
      logger.plain("  Expected a full UUID (e.g. beb47f34-fdf8-49c4-9b9f-96bd367ed145).");
      logger.info("Run `vibesku status <job-id>` to see full output IDs.");
      process.exit(1);
    }
    const spinner = new Spinner("Fetching outputs...").start();
    try {
      const { data } = await api.downloadJob(jobId, opts.outputId);
      spinner.stop();
      if (opts.json) {
        logger.plain(formatJson(data));
        return;
      }
      if (data.outputs.length === 0) {
        logger.warn("No outputs found for this job.");
        return;
      }
      await (0, import_promises.mkdir)(opts.outputDir, { recursive: true });
      let downloadCount = 0;
      for (const output of data.outputs) {
        if (output.type === "IMAGE" && output.imageUrl) {
          const dlSpinner = new Spinner(`Downloading ${output.id.slice(0, 8)}...`).start();
          try {
            const res = await fetch(output.imageUrl);
            if (!res.ok) {
              dlSpinner.fail(`Failed to download ${output.id.slice(0, 8)}`);
              continue;
            }
            const buffer = Buffer.from(await res.arrayBuffer());
            const ext = output.imageUrl.includes(".png") ? ".png" : output.imageUrl.includes(".webp") ? ".webp" : ".jpg";
            const fileName = `${output.id}${ext}`;
            await (0, import_promises.writeFile)((0, import_node_path2.join)(opts.outputDir, fileName), buffer);
            dlSpinner.succeed(`Saved ${fileName}`);
            downloadCount++;
          } catch {
            dlSpinner.fail(`Failed to download ${output.id.slice(0, 8)}`);
          }
        } else if (output.type === "TEXT" && output.content) {
          const fileName = `${output.id}.txt`;
          await (0, import_promises.writeFile)((0, import_node_path2.join)(opts.outputDir, fileName), output.content);
          logger.success(`Saved ${fileName}`);
          downloadCount++;
        }
      }
      logger.plain("");
      logger.success(`Downloaded ${downloadCount}/${data.outputs.length} outputs to ${opts.outputDir}`);
    } catch (error) {
      spinner.fail("Failed to export outputs.");
      if (error instanceof ApiError) {
        if (error.code === "JOB_NOT_FOUND") {
          logger.error(`Job '${jobId}' not found.`);
        } else if (error.code === "OUTPUT_NOT_FOUND") {
          logger.error(`Output '${opts.outputId}' not found in job '${jobId}'.`);
        } else {
          logger.error(`${error.code}: ${error.message}`);
        }
      } else if (error instanceof Error) {
        logger.error(error.message);
      }
      process.exit(1);
    }
  }
);

// src/commands/batch.ts
var batchCommand = new Command("batch").description("Run batch generation from a JSON file").argument("<file>", "Path to batch JSON file").option("--json", "Output results as JSON").option("--dry-run", "Validate the file without submitting").action(async (file, opts) => {
  let items;
  try {
    items = (0, import_batch_file.loadBatchItems)(file);
  } catch (error) {
    if (error instanceof Error) {
      logger.error(error.message);
    } else {
      logger.error("Failed to parse batch file as JSON.");
    }
    process.exit(1);
  }
  logger.info(`Found ${items.length} items in batch file.`);
  if (opts.dryRun) {
    logger.success("Dry run: file is valid.");
    return;
  }
  const results = [];
  for (let i = 0; i < items.length; i++) {
    const item = items[i];
    const spinner = new Spinner(`[${i + 1}/${items.length}] Generating ${item.templateId}...`).start();
    try {
      const { data } = await api.generate({
        templateId: item.templateId,
        brief: item.brief,
        assetIds: item.assetIds,
        options: item.options
      });
      spinner.succeed(`[${i + 1}/${items.length}] Job ${data.jobId} started.`);
      results.push({ index: i, jobId: data.jobId });
    } catch (error) {
      const msg = error instanceof Error ? error.message : "Unknown error";
      spinner.fail(`[${i + 1}/${items.length}] Failed: ${msg}`);
      results.push({ index: i, error: msg });
    }
  }
  logger.plain("");
  const succeeded = results.filter((r) => r.jobId).length;
  const failed = results.filter((r) => r.error).length;
  logger.info(`Batch complete: ${succeeded} succeeded, ${failed} failed.`);
  if (opts.json) {
    logger.plain(formatJson(results));
  } else {
    for (const r of results) {
      if (r.jobId) {
        logger.plain(`  [${r.index}] ${r.jobId}`);
      } else {
        logger.plain(`  [${r.index}] ERROR: ${r.error}`);
      }
    }
  }
});

// src/commands/auth.ts
var import_node_os3 = require("os");
function resolveBaseUrl(baseUrlFlag) {
  if (baseUrlFlag) {
    const url = baseUrlFlag.replace(/\/$/, "");
    const config = loadConfig();
    config.baseUrl = url;
    saveConfig(config);
    return url;
  }
  return getBaseUrl();
}
var authCommand = new Command("auth").description(
  "Manage authentication"
);
authCommand.command("login").description("Sign in via browser-based device authorization").option("--no-browser", "Print the URL instead of opening a browser").option("--base-url <url>", "Custom API base URL").action(async (opts) => {
  const baseUrl = resolveBaseUrl(opts.baseUrl);
  const isTTY = process.stdout.isTTY;
  const shouldOpenBrowser = opts.browser && !!isTTY;
  const clientName = `${(0, import_node_os3.hostname)()} (${(0, import_node_os3.type)()})`;
  const cliVersion = "0.1.0";
  let spinner = new Spinner("Requesting device code...").start();
  let deviceCode;
  let userCode;
  let interval;
  let expiresIn;
  try {
    const res = await fetch(`${baseUrl}/api/v1/device/code`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ clientName, clientVersion: cliVersion })
    });
    const envelope = await res.json();
    if (!envelope.success || !envelope.data) {
      spinner.fail("Failed to request device code.");
      logger.error(envelope.error?.message ?? "Unknown error");
      process.exit(1);
    }
    deviceCode = envelope.data.deviceCode;
    userCode = envelope.data.userCode;
    interval = envelope.data.interval;
    expiresIn = envelope.data.expiresIn;
  } catch (error) {
    spinner.fail("Failed to connect to server.");
    if (error instanceof Error) logger.error(error.message);
    process.exit(1);
  }
  spinner.succeed("Device code received!");
  logger.plain("");
  logger.plain("  Your one-time code:");
  logger.plain("");
  logger.plain(`    ${c("bold", c("cyan", userCode))}`);
  logger.plain("");
  const fullUrl = `${baseUrl}/device?code=${encodeURIComponent(userCode)}`;
  if (shouldOpenBrowser) {
    logger.info(`Opening browser to authorize...`);
    openBrowser(fullUrl);
  } else {
    logger.plain(`  Open this URL in your browser:`);
    logger.plain(`  ${fullUrl}`);
  }
  logger.plain("");
  spinner = new Spinner("Waiting for authorization...").start();
  let pollInterval = interval;
  let consecutiveErrors = 0;
  const startTime = Date.now();
  const deadline = startTime + expiresIn * 1e3;
  let cancelled = false;
  const onSigint = () => {
    cancelled = true;
    spinner.fail("Login cancelled.");
    process.exit(0);
  };
  process.on("SIGINT", onSigint);
  try {
    while (!cancelled && Date.now() < deadline) {
      await sleep(pollInterval * 1e3);
      if (cancelled) break;
      const elapsed = Date.now() - startTime;
      if (elapsed > 12e4 && elapsed < 12e4 + pollInterval * 1e3 + 500) {
        spinner.stop();
        logger.dim(`  Try opening the URL manually: ${fullUrl}`);
        spinner = new Spinner("Still waiting for authorization...").start();
      } else if (elapsed > 3e4 && elapsed < 3e4 + pollInterval * 1e3 + 500) {
        spinner.stop();
        spinner = new Spinner("Still waiting...").start();
      }
      try {
        const res = await fetch(`${baseUrl}/api/v1/device/token`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ deviceCode })
        });
        const envelope = await res.json();
        consecutiveErrors = 0;
        if (!envelope.success || !envelope.data) {
          spinner.fail("Unexpected server error.");
          logger.error(envelope.error?.message ?? "Unknown error");
          process.exit(1);
        }
        const data = envelope.data;
        if (data.accessToken && data.refreshToken) {
          const config = loadConfig();
          config.accessToken = data.accessToken;
          config.refreshToken = data.refreshToken;
          config.tokenExpiresAt = new Date(
            Date.now() + (data.expiresIn ?? 7776e3) * 1e3
          ).toISOString();
          saveConfig(config);
          spinner.succeed("Authenticated!");
          logger.plain("");
          try {
            const verifyRes = await api.authVerify();
            const user = verifyRes.data.user;
            logger.plain(
              `  Welcome, ${user.name || user.email}!`
            );
            logger.plain(`  Credits: ${verifyRes.data.plan.creditsRemaining}`);
          } catch {
          }
          logger.plain(`  Config:  ${getConfigPath()}`);
          logger.plain("");
          logger.info(
            "Run `vibesku templates` to see available templates."
          );
          return;
        }
        if (data.status === "expired") {
          spinner.fail("Code expired. Please try again.");
          process.exit(1);
        }
        if (data.status === "slow_down") {
          pollInterval = Math.min(pollInterval + 1, 30);
        }
      } catch {
        consecutiveErrors++;
        if (consecutiveErrors >= 3) {
          spinner.fail(
            "Network error. Please check your connection and try again."
          );
          process.exit(1);
        }
        await sleep(2e3);
      }
    }
    if (!cancelled) {
      spinner.fail("Authorization timed out. Please try again.");
      process.exit(1);
    }
  } finally {
    process.off("SIGINT", onSigint);
  }
});
authCommand.command("logout").description("Sign out and clear stored credentials").action(async () => {
  const baseUrl = getBaseUrl();
  const config = loadConfig();
  if (config.accessToken) {
    try {
      await fetch(`${baseUrl}/api/v1/auth/verify`, {
        method: "GET",
        headers: { Authorization: `Bearer ${config.accessToken}` }
      });
    } catch {
    }
  }
  config.accessToken = void 0;
  config.refreshToken = void 0;
  config.tokenExpiresAt = void 0;
  saveConfig(config);
  logger.success("Logged out. Stored token cleared.");
  if (config.apiKey) {
    logger.dim("  Note: API key is still configured. Use `vibesku config set-key` to manage.");
  }
});
authCommand.command("status").description("Show current authentication status").action(async () => {
  const config = loadConfig();
  const token = getAuthToken();
  logger.plain(`  Config:  ${getConfigPath()}`);
  logger.plain(`  Server:  ${getBaseUrl()}`);
  logger.plain("");
  if (!token) {
    logger.warn(
      "Not authenticated. Run `vibesku auth login` to sign in."
    );
    return;
  }
  if (token.startsWith("vst_")) {
    logger.plain("  Auth:    CLI Token (browser login)");
    if (config.tokenExpiresAt) {
      const expires = new Date(config.tokenExpiresAt);
      const remaining = expires.getTime() - Date.now();
      if (remaining <= 0) {
        logger.warn("  Token expired. Run `vibesku auth login` to re-authenticate.");
        return;
      }
      const days = Math.floor(remaining / (1e3 * 60 * 60 * 24));
      logger.plain(`  Expires: ${expires.toLocaleDateString()} (${days} days)`);
    }
  } else if (token.startsWith("vsk_")) {
    const source = (0, import_config_store.hasEnvApiKey)() ? "env var" : "config file";
    logger.plain(`  Auth:    API Key (${source})`);
  }
  const spinner = new Spinner("Verifying...").start();
  try {
    const { data } = await api.authVerify();
    spinner.succeed("Authenticated");
    logger.plain(`  User:    ${data.user.name || data.user.email}`);
    logger.plain(`  Credits: ${data.plan.creditsRemaining}`);
  } catch (error) {
    spinner.fail("Token verification failed.");
    if (error instanceof Error) logger.error(error.message);
  }
});
authCommand.command("refresh").description("Manually refresh the CLI token").action(async () => {
  const baseUrl = getBaseUrl();
  const config = loadConfig();
  if (!config.refreshToken) {
    logger.error(
      "No refresh token found. Run `vibesku auth login` to sign in."
    );
    process.exit(1);
  }
  const spinner = new Spinner("Refreshing token...").start();
  try {
    const res = await fetch(`${baseUrl}/api/v1/device/refresh`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ refreshToken: config.refreshToken })
    });
    const envelope = await res.json();
    if (!envelope.success || !envelope.data) {
      spinner.fail("Token refresh failed.");
      logger.error(
        envelope.error?.message ?? "Please run `vibesku auth login` to re-authenticate."
      );
      process.exit(1);
    }
    config.accessToken = envelope.data.accessToken;
    config.refreshToken = envelope.data.refreshToken;
    config.tokenExpiresAt = new Date(
      Date.now() + envelope.data.expiresIn * 1e3
    ).toISOString();
    saveConfig(config);
    spinner.succeed("Token refreshed!");
    const expires = new Date(config.tokenExpiresAt);
    const days = Math.floor(
      (expires.getTime() - Date.now()) / (1e3 * 60 * 60 * 24)
    );
    logger.plain(`  Expires: ${expires.toLocaleDateString()} (${days} days)`);
  } catch (error) {
    spinner.fail("Failed to connect to server.");
    if (error instanceof Error) logger.error(error.message);
    process.exit(1);
  }
});
function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

// src/commands/refine.ts
var refineCommand = new Command("refine").description("Refine an existing output with new instructions").argument("<output-id>", "Output ID to refine").requiredOption("-p, --prompt <text>", "Edit instruction").option("--aspect-ratio <ratio>", "Override aspect ratio (e.g. 3:2, 1:1)").option("--image-size <size>", "Image size (1K, 2K, 4K)").option("-y, --yes", "Skip confirmation").option("--json", "Output as JSON").action(async (outputId, opts) => {
  const {
    prompt,
    aspectRatio,
    imageSize,
    yes: skipConfirm,
    json: jsonOutput
  } = opts;
  const UUID_RE = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
  if (!UUID_RE.test(outputId)) {
    logger.error(`Invalid output ID format: '${outputId}'`);
    logger.plain("  Expected a full UUID (e.g. beb47f34-fdf8-49c4-9b9f-96bd367ed145).");
    logger.info("Run `vibesku status <job-id> --json` to see full output IDs.");
    process.exit(1);
  }
  if (!skipConfirm) {
    const { createInterface: createInterface2 } = await import("readline");
    const rl = createInterface2({ input: process.stdin, output: process.stdout });
    const answer = await new Promise((resolve) => {
      rl.question("Refining will consume credits. Continue? (y/N) ", resolve);
    });
    rl.close();
    if (answer.toLowerCase() !== "y") {
      logger.info("Cancelled.");
      return;
    }
  }
  const req = {
    instruction: prompt,
    options: aspectRatio || imageSize ? {
      aspectRatio,
      imageSize
    } : void 0
  };
  const spinner = new Spinner("Starting refine...").start();
  try {
    const { data } = await api.refine(outputId, req);
    spinner.succeed("Refine started!");
    if (jsonOutput) {
      logger.plain(formatJson(data));
    } else {
      logger.plain("");
      logger.plain(`  Run ID:             ${data.runId}`);
      logger.plain(`  Job ID:             ${data.jobId}`);
      logger.plain(`  Status:             ${data.status}`);
      logger.plain(`  Credits remaining:  ${formatCredits(data.creditsRemaining)}`);
      logger.plain("");
      logger.info(`Track progress with: vibesku status ${data.jobId}`);
    }
  } catch (error) {
    spinner.fail("Refine failed.");
    if (error instanceof ApiError && error.code === "INSUFFICIENT_CREDITS") {
      const details = error.details;
      const required = details?.required ?? "unknown";
      const available = details?.available ?? "unknown";
      logger.error(`Insufficient credits: ${required} required, ${available} available.`);
      logger.plain("");
      logger.info("Run `vibesku credits buy` to purchase credits.");
      logger.info("Run `vibesku credits redeem <code>` to redeem a code.");
    } else if (error instanceof ApiError && error.code === "OUTPUT_NOT_FOUND") {
      logger.error(`Output '${outputId}' not found.`);
    } else if (error instanceof Error) {
      logger.error(error.message);
    }
    process.exit(1);
  }
});

// bin/vibesku.ts
var program2 = new Command();
program2.name("vibesku").description("VibeSKU CLI - AI-powered product image generation").version("0.1.0");
program2.addCommand(initCommand);
program2.addCommand(configCommand);
program2.addCommand(templatesCommand);
program2.addCommand(creditsCommand);
program2.addCommand(generateCommand);
program2.addCommand(statusCommand);
program2.addCommand(jobsCommand);
program2.addCommand(exportCommand);
program2.addCommand(batchCommand);
program2.addCommand(authCommand);
program2.addCommand(refineCommand);
program2.parse();
