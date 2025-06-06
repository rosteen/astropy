#-----------------------------------------------------------------------------
# Process this file with autoconf-2.53 or later to produce a configure script.
#-----------------------------------------------------------------------------
# Author: Mark Calabretta, Australia Telescope National Facility, CSIRO.
# http://www.atnf.csiro.au/people/Mark.Calabretta
# $Id: configure.ac,v 8.4 2024/10/28 13:56:17 mcalabre Exp $
#-----------------------------------------------------------------------------

AC_INIT([WCSLIB],[8.4],[mark@calabretta.id.au],[wcslib-8.4])
AC_PREREQ([2.71])
AC_REVISION([$Revision: 8.4 $])
AC_SUBST([PACKAGE_VERSION])
AC_DEFINE_UNQUOTED([WCSLIB_VERSION], [$PACKAGE_VERSION], [Define wcslib version])

# Library version number, same as package version.
LIBVER="$PACKAGE_VERSION"
AC_SUBST([LIBVER])

AC_CONFIG_SRCDIR([C/wcs.h])
AC_CONFIG_AUX_DIR([config])

# Get the system type.
AC_CANONICAL_HOST
ARCH="${host_cpu}-$host_os"
AC_SUBST([ARCH])


# Look for Flex.
AC_ARG_ENABLE([flex], [AS_HELP_STRING([--disable-flex],
            [don't apply flex (use pre-generated sources)])], [])
if test "x$enable_flex" = xno ; then
  FLEX=
  AC_MSG_WARN([Generation of flex sources disabled by request, using
           pre-generated sources.])

else
  AC_CHECK_PROG([FLEX], [flex], [flex], [], [], [])
  if test "x$FLEX" = xflex ; then
    # Version 2.6.0 or later is required.
    V=`flex --version | awk '{print $2}'`
    W=`echo $V | awk -F. '{if ((($1*100 + $2)*100 + $3) < 20600) print "no"}'`
    if test "x$W" != x ; then
      AC_MSG_WARN([Flex version $V is too old, ignored.])
      FLEX=
    else
      AC_MSG_NOTICE([Using Flex version $V.])
    fi
  fi

  if test "x$FLEX" = x ; then
    AC_MSG_WARN([Flex version 2.6.0 or later does not appear to be
           available, will use pre-generated sources.])
  fi
fi


# Look for an ANSI C compiler.
AC_PROG_CPP
AC_PROG_CC
if test "x$ac_cv_c_compiler_gnu" = xyes ; then
  # Get gcc version number.
  GCC_VERSION=`$CC -dumpfullversion`
  AC_MSG_NOTICE([Using gcc version $GCC_VERSION])
else
  GCC_VERSION=
fi
AC_SUBST([GCC_VERSION])

AC_C_CONST
AC_TYPE_SIZE_T
if test "x$ac_cv_prog_cc_stdc" = xno -o \
        "x$ac_cv_c_const"      = xno -o \
        "x$ac_cv_type_size_t"  = xno; then
  AC_MSG_ERROR([
    -------------------------------------------------------
    An ANSI standard C library is required to build WCSLIB.

    ERROR: WCSLIB configuration failure.
    -------------------------------------------------------], [1])
fi

# Data types used in wcs.c (results not currently used).
AC_TYPE_UINT16_T
AC_TYPE_UINT32_T

# Check for standard C header files required to compile the library.
headers=
AC_CHECK_HEADERS([ctype.h inttypes.h limits.h locale.h math.h setjmp.h
                  stdarg.h stddef.h stdint.h stdio.h stdlib.h string.h],
                  [], [headers=no])
if test "x$headers" = xno; then
  AC_MSG_ERROR([
    -------------------------------------------------------------------
    An ANSI standard C library is required to build WCSLIB.  One of the
    standard C header files it requires is missing or unusable.  Please
    refer to the above log.

    ERROR: WCSLIB configuration failure.
    -------------------------------------------------------------------], [1])
fi

# Flex uses fileno() and other POSIX features whose prototypes are only
# available from glibc's stdio.h with an appropriate preprocessor macro
# definition.  This cannot be set within the flex description file itself
# as stdio.h is included in the generated C code before any part of the
# description.  See fileno(3) and feature_test_macros(7).
if test "x$ac_cv_c_compiler_gnu" = xyes ; then
  FLFLAGS="$FLFLAGS -D_POSIX_C_SOURCE=1"
fi
AC_SUBST([FLFLAGS])

# Check for libm.
AC_CHECK_LIB([m], [floor])

# System libraries that may be required by WCSLIB itself.
# SunOS, extra maths functions.
AC_CHECK_LIB([sunmath], [cosd], [LIBS="-lsunmath $LIBS"], [], [])

# See if we can find sincos().
AC_CHECK_FUNCS([sincos])

# Check the size and availability of integer data types.
AC_CHECK_SIZEOF([int])
AC_CHECK_SIZEOF([long int])
AC_CHECK_SIZEOF([long long int])

# 64-bit integer data type; use long long int preferentially since that
# accords with "%lld" formatting used in fitshdr.l, e.g.
#                int   size_t  long int  long long int
#                ---   ------  --------  -------------
#   gcc x86:      32     32       32          64
#   gcc x86_64:   32     64       64          64
if test "x$ac_cv_sizeof_long_long_int" = x8; then
  AC_DEFINE([WCSLIB_INT64], [long long int], [64-bit integer data type.])
elif test "x$ac_cv_sizeof_long_int" = x8; then
  AC_DEFINE([WCSLIB_INT64], [long int], [64-bit integer data type.])
elif test "x$ac_cv_sizeof_int" = x8; then
  AC_DEFINE([WCSLIB_INT64], [int], [64-bit integer data type.])
fi

# Does printf() have the z modifier for size_t type?  Important for 64-bit.
AC_MSG_CHECKING([for printf z format modifier for size_t type])
AC_RUN_IFELSE(
  [AC_LANG_PROGRAM([AC_INCLUDES_DEFAULT],
                   [[char buf[64];
                     if (sprintf(buf, "%zu", (size_t)1) != 1)
                       return 1;
                     else if (strcmp(buf, "1"))
                       return 2;]])],
  AC_DEFINE([MODZ], ["z"], [printf format modifier for size_t type.])
    AC_MSG_RESULT(yes),
  AC_DEFINE([MODZ], [""],  [printf format modifier for size_t type.])
    AC_MSG_RESULT(no),
  AC_DEFINE([MODZ], [""],  [printf format modifier for size_t type.])
    AC_MSG_RESULT(assumed not)
)


# Starting values, may be augmented later.
SUBDIRS="C"
TSTDIRS="C"
INSTDIR="C"


# Ways of specifying the Fortran compiler, in order of precedence:
#   configure --enable-fortran=<compiler>
#   F77=<compiler> configure    ...bash
#
# Ways of disabling Fortran:
#   configure --disable-fortran
#   configure --enable-fortran=no
#   F77=no configure            ...bash
AC_ARG_ENABLE([fortran], [AS_HELP_STRING([--enable-fortran=ARG],
            [Fortran compiler to use])], [])
AC_ARG_ENABLE([fortran], [AS_HELP_STRING([--disable-fortran],
            [don't build the Fortran wrappers or PGSBOX])], [])
if test "x$enable_fortran" != x -a "x$enable_fortran" != xyes ; then
  F77="$enable_fortran"
fi

if test "x$F77" = xno ; then
  F77=

  AC_MSG_WARN([Compilation of Fortran wrappers and PGSBOX disabled.])

else
  if test "x$F77" = x ; then
    # Look for a Fortran compiler.
    AC_PROG_F77([gfortran g77 f77 ifort xlf frt pgf77 fl32 af77 fort77 f90 \
                 xlf90 pgf90 epcf90 f95 fort xlf95 lf95 g95])
  fi

  if test "x$F77" = x; then
    AC_MSG_WARN([
      ------------------------------------------------------------------
      Fortran compiler not found, will skip Fortran wrappers and PGSBOX.
      ------------------------------------------------------------------])

    # Best guess at Fortran name mangling for use if a compiler does ever
    # become available.
    AC_DEFINE([F77_FUNC(name,NAME)], [name ## _])

  else
    if test "x$ac_cv_f77_compiler_gnu" = xyes ; then
      if test "x$F77" = xg77 -o "x$F77" = xf77 ; then
        # Not recognized by gfortran.
        FFLAGS="$FFLAGS -Wno-globals"
      fi
    fi

    AC_MSG_CHECKING(whether $F77 accepts -I)
    AC_LANG_PUSH(Fortran 77)
    FFLAGS_save=$FFLAGS
    FFLAGS=-I.
    AC_COMPILE_IFELSE(AC_LANG_PROGRAM([], []),
      [FFLAGS="$FFLAGS_save -I."; AC_MSG_RESULT(yes)],
      [FFLAGS="$FFLAGS_save"; AC_MSG_RESULT(no)])
    AC_LANG_POP()

    # Libraries required by the Fortran compiler itself (sets FLIBS).
    # Required by utilities and test programs written in C that link to
    # Fortran object modules such as pgsbox.
    AC_F77_LIBRARY_LDFLAGS

    # Tidy up FLIBS.
    dirs=
    libs=
    for flib in $FLIBS
    do
      case "$flib" in
      -L*)  
        dir=`echo "$flib" | sed -e 's/-L//'`
        dir=-L`cd "$dir" && pwd`
        dirs="$dirs $dir"
        ;;  
      *) 
        libs="$libs $flib"
        ;;  
      esac
    done

    dirs=`for dir in $dirs ; do echo "$dir" ; done | sort -u | xargs`

    FLIBS="$dirs$libs"

    # F77 name mangling (defines the F77_FUNC preprocessor macro).
    AC_F77_WRAPPERS

    if test "x$BINDC" = x ; then
      AC_ARG_WITH([bindc], [AS_HELP_STRING([--with-bindc],
              [use Fortran 2003 BIND(C) wrappers - recommended for Link Time
               Optimization (LTO)])], [])
      if test "x$with_bindc" = xyes ; then
        BINDC=yes
      fi
    fi

    if test "x$BINDC" = xyes ; then
      AC_MSG_NOTICE([using Fortran 2003 BIND(C) wrappers.])
    else
      BINDC=
    fi
    AC_SUBST([BINDC])

    SUBDIRS="C Fortran"
    TSTDIRS="C Fortran"
    INSTDIR="Fortran"
  fi
fi


# System-dependent system libraries (for building the sharable library).
#-----------------------------------------------------------------------
# Darwin (contains stubs for long double).
AC_CHECK_LIB([SystemStubs], [printf\$LDBLStub], [LIBS="$LIBS -lSystemStubs"],
             [], [])


# Library and installation utilities.
#------------------------------------
# Static library generation.
# Ensure "non-deterministic" archives are produced during the build process.
ar rU conftest.a > /dev/null 2>&1 && ARFLAGS="U"
rm -f conftest.a
AC_SUBST([ARFLAGS])
AC_PROG_RANLIB

# Shared library generation - gcc only.
# Ways of disabling shared libraries:
#   configure --disable-shared
#   configure --enable-shared=no
AC_ARG_ENABLE([shared], [AS_HELP_STRING([--disable-shared],
            [don't build the WCS shared libraries])], [])

SHRLIB=
SONAME=
SHRFLAGS=
SHRLD=
SHRSFX=
SHRLN=

if test "x$ac_cv_c_compiler_gnu" = xyes ; then
  if test "x$enable_shared" = xno ; then
    AC_MSG_WARN([Generation of WCS shared libraries disabled.])

  else
    SHVER=`echo "$LIBVER" | sed -e 's/\..*$//'`

    # Note that -fPIC is on by default for Macs, this just makes it obvious.
    SHRFLAGS="-fPIC"
    SHRLD="\$(CC) \$(SHRFLAGS)"

    case "$host_os" in
    darwin*)
      SHRLIB="libwcs.$LIBVER.dylib"
      SONAME="libwcs.$SHVER.dylib"
      SHRLD="$SHRLD -dynamiclib -single_module"
      SHRLD="$SHRLD -compatibility_version $SHVER -current_version $LIBVER -install_name \$(SONAME)"
      SHRLN="libwcs.dylib"

      case "$host_cpu" in
      powerpc*)
        # Switch off -fPIC (not applicable for PowerPC Macs).
        CFLAGS="$CFLAGS -mdynamic-no-pic"
        ;;
      esac
      ;;
    *mingw*)
      SHRLIB="libwcs.dll.$LIBVER"
      SONAME="libwcs.dll.$SHVER"
      SHRLD="$SHRLD -shared -Wl,-h\$(SONAME)"
      SHRLN="libwcs.dll"
      ;;
    *)
      # Covers Linux and Solaris at least.
      SHRLIB="libwcs.so.$LIBVER"
      SONAME="libwcs.so.$SHVER"
      SHRLD="$SHRLD -shared -Wl,-h\$(SONAME)"
      SHRLN="libwcs.so"
      ;;
    esac
  fi
fi

AC_SUBST([SHRLIB])
AC_SUBST([SONAME])
AC_SUBST([SHRFLAGS])
AC_SUBST([SHRLD])
AC_SUBST([SHRSFX])
AC_SUBST([SHRLN])

# Installation utilities.
AC_PROG_LN_S
AC_PROG_INSTALL

# Older versions of GNU make do not have the -O option, which only facilitates
# legibility of the output from parallel builds (make -j).
make --help | grep '\-O' >/dev/null 2>&1 && MAKEFLAGS="-Otarget"
AC_SUBST([MAKEFLAGS])

AC_MSG_NOTICE([End of primary configuration.
])


# The following are required to build utilities and test programs.
# ----------------------------------------------------------------
AC_MSG_NOTICE([Looking for libraries etc. for utilities and test suite...])

# Additional standard C header files required.
headers=
AC_CHECK_HEADERS([errno.h time.h], [], [headers=no])

# Other header files required by *nix library functions.
AC_CHECK_HEADERS([sys/stat.h sys/types.h unistd.h], [], [headers=no])
if test "x$headers" = xno; then
  AC_MSG_WARN([
    --------------------------------------------------------------------
    One or more of the header files required to compile the utilities
    and/or test programs is missing.  Continuing on a best-effort basis.
    --------------------------------------------------------------------])
fi

# Large file support (only required by fitshdr utility).
AC_FUNC_FSEEKO
AC_SYS_LARGEFILE
AC_TYPE_OFF_T

# Extra places to look for third-party libraries and header files.
LIBDIRS=

AC_ARG_WITH([cfitsio], [AS_HELP_STRING([--without-cfitsio],
            [eschew CFITSIO])], [])
if test "x$with_cfitsio" = xno ; then
  AC_MSG_WARN([CFITSIO disabled.])
else
  AC_ARG_WITH([cfitsiolib], [AS_HELP_STRING([--with-cfitsiolib=DIR],
              [directory containing cfitsio library])], [])
  if test "x$with_cfitsiolib" != x ; then
    LIBDIRS="$LIBDIRS $with_cfitsiolib"
  fi

  AC_ARG_WITH([cfitsioinc], [AS_HELP_STRING([--with-cfitsioinc=DIR],
              [directory containing cfitsio header files])], [])
  if test "x$with_cfitsioinc" != x ; then
    CFITSIO_INCDIRS="$with_cfitsioinc"
  fi

  CFITSIO_INCDIRS="$CFITSIO_INCDIRS   \
           /usr/local/cfitsio/include \
           /local/cfitsio/include"

  LIBDIRS="$LIBDIRS           \
           /usr/local/cfitsio/lib \
           /local/cfitsio/lib"
fi

AC_ARG_WITH([pgplot], [AS_HELP_STRING([--without-pgplot],
            [eschew PGPLOT])], [])
if test "x$with_pgplot" = xno ; then
  AC_MSG_WARN([PGPLOT disabled.])
else
  AC_ARG_WITH([pgplotlib], [AS_HELP_STRING([--with-pgplotlib=DIR],
              [directory containing pgplot library])], [])
  if test "x$with_pgplotlib" != x ; then
    LIBDIRS="$LIBDIRS $with_pgplotlib"
  fi

  AC_ARG_WITH([pgplotinc], [AS_HELP_STRING([--with-pgplotinc=DIR],
              [directory containing pgplot header files])], [])
  if test "x$with_pgplotinc" != x ; then
    PGPLOT_INCDIRS="$with_pgplotinc"
  fi

  PGPLOT_INCDIRS="$PGPLOT_INCDIRS    \
           /usr/local/pgplot/include \
           /local/pgplot/include"

  LIBDIRS="$LIBDIRS           \
           /usr/local/pgplot/lib  \
           /local/pgplot/lib"
fi


if test "x$with_cfitsio" != xno -o \
        "x$with_pgplot"  != xno ; then
  LIBDIRS="$LIBDIRS           \
           /usr/local/lib     \
           /local/lib         \
           /opt/local/lib     \
           /opt/SUNWspro/lib  \
           /sw/lib"

  for LIBDIR in $LIBDIRS ; do
    AC_CHECK_FILE([$LIBDIR], [LDFLAGS="$LDFLAGS -L$LIBDIR"], [continue])
  done

  # Generic include directories.
  INCDIRS="/usr/local/include \
           /local/include     \
           /opt/local/include \
           /sw/include        \
           /local             \
           /usr/include"


  # CFITSIO.
  if test "x$with_cfitsio" != xno ; then
    # Search for CFITSIO.
    for INCDIR in $CFITSIO_INCDIRS $INCDIRS ; do
      AC_CHECK_FILE([$INCDIR/cfitsio/fitsio.h],
                    [CFITSIOINC="-I$INCDIR/cfitsio"; break])
      AC_CHECK_FILE([$INCDIR/fitsio.h], [CFITSIOINC="-I$INCDIR"; break])
    done

    AC_CHECK_LIB([socket],  [recv],   [CFITSIOLIB="-lsocket"], [], [$LIBS])
    AC_CHECK_LIB([cfitsio], [ffopen], [CFITSIOLIB="-lcfitsio $CFITSIOLIB"], [],
                 [$CFITSIOLIB $LIBS])

    if test "x$CFITSIOINC" = x -o "x$CFITSIOLIB" = x; then
      AC_MSG_WARN([CFITSIO not found, skipping CFITSIO-dependent tests.])
    else
      AC_MSG_NOTICE([CFITSIO appears to be available.])
      AC_DEFINE([HAVE_CFITSIO], [1], [Define to 1 if CFITSIO is available.])

      # Check for fits_read_wcstab, present in CFITSIO 3.004beta and later.
      AC_CHECK_LIB([cfitsio], [fits_read_wcstab], [GETWCSTAB=],
                   [GETWCSTAB=getwcstab.o], [$CFITSIOLIB $LIBS])
      if test "x$GETWCSTAB" != x ; then
        AC_MSG_WARN([fits_read_wcstab not found in CFITSIO, will use
                        getwcstab.c to compile test programs.])
      fi
    fi

    AC_SUBST([CFITSIOINC])
    AC_SUBST([CFITSIOLIB])
    AC_SUBST([GETWCSTAB])
  fi

  # PGPLOT.
  if test "x$F77" != x -a "x$with_pgplot" != xno ; then
    # Search for PGPLOT.
    for INCDIR in $PGPLOT_INCDIRS $INCDIRS ; do
      AC_CHECK_FILE([$INCDIR/pgplot/cpgplot.h],
                    [PGPLOTINC="-I$INCDIR/pgplot"; break])
      AC_CHECK_FILE([$INCDIR/cpgplot.h], [PGPLOTINC="-I$INCDIR"; break])
    done

    # FLIBS (found above via AC_F77_LIBRARY_LDFLAGS) only helps if PGPLOT was
    # built using the same Fortran compiler that we are using here.

    # PGPLOT compiled by the SUN Fortran compiler but linked with something
    # else.
    AC_CHECK_LIB([M77],     [iand_],     [PGPLOTLIB="-lM77 $PGPLOTLIB"],
                 [], [$PGPLOTLIB $LIBS])
    AC_CHECK_LIB([F77],     [f77_init],  [PGPLOTLIB="-lF77 $PGPLOTLIB"],
                 [], [$PGPLOTLIB $LIBS])

    if test "x$F77" != xg77; then
      # For PGPLOT compiled with g77 but linked with something else.
      AC_CHECK_LIB([frtbegin], [main],     [PGPLOTLIB="-lfrtbegin $PGPLOTLIB"],
                   [], [$PGPLOTLIB $LIBS])
      AC_CHECK_LIB([g2c],      [gerror_],  [PGPLOTLIB="-lg2c $PGPLOTLIB"],
                   [], [$PGPLOTLIB $LIBS])
    fi

    if test "x$F77" != xgfortran; then
      # For PGPLOT compiled with gfortran but linked with something else.
      # Note that if gfortran itself is driving the linker it can be harmful
      # to add -lgfortran to the link list without also adding -lgfortranbegin.
      # Doing so stops gfortran from adding -lgfortranbegin which is needed to
      # resolve "main".
      AC_CHECK_LIB([gfortran], [_gfortran_abort],
                   [PGPLOTLIB="-lgfortran $PGPLOTLIB"], [],
                   [$PGPLOTLIB $LIBS])
    fi

    # Search for X11 includes and libraries.
    AC_PATH_X
    if test "x$no_x" = x; then
      if test "x$ac_x_libraries" != x ; then
        # Not needed for systems that keep the X11 libraries in /usr/lib.
        LDFLAGS="$LDFLAGS -L$ac_x_libraries"
      fi
      PGPLOTLIB="-lX11 $PGPLOTLIB"
    fi

    # It is possible that other libraries may be required depending on what
    # graphics drivers were installed with PGPLOT.
    AC_CHECK_LIB([z],       [deflate],   [PGPLOTLIB="-lz $PGPLOTLIB"],
                 [], [$PGPLOTLIB $LIBS])
    AC_CHECK_LIB([png],     [png_error], [PGPLOTLIB="-lpng $PGPLOTLIB"],
                 [], [$PGPLOTLIB $LIBS])
    AC_CHECK_LIB([pgplot],  [pgbeg_],    [PGPLOTLIB="-lpgplot $PGPLOTLIB"],
                 [], [$PGPLOTLIB $FLIBS $LIBS])
    AC_CHECK_LIB([cpgplot], [cpgbeg],    [PGPLOTLIB="-lcpgplot $PGPLOTLIB"],
                 [PGPLOTLIB=], [$PGPLOTLIB $FLIBS $LIBS])

    # Only need the PGPLOT include file to build PGSBOX.
    if test "x$PGPLOTINC" != x; then
      SUBDIRS="$SUBDIRS pgsbox"
      INSTDIR="pgsbox"
    fi

    # Also need the PGPLOT library to build pgtest and cpgtest.
    if test "x$PGPLOTLIB" = x; then
      AC_MSG_WARN([PGPLOT not found, skipping PGPLOT-dependent tests.])
    else
      AC_MSG_NOTICE([PGPLOT appears to be available.])

      TSTDIRS="$TSTDIRS pgsbox"
    fi
  fi

  AC_SUBST([PGPLOTINC])
  AC_SUBST([PGPLOTLIB])
fi


# Utilities are compiled last since they need the libraries.
# Ways of disabling them:
#   configure --disable-utils
#   configure --enable-utils=no
AC_ARG_ENABLE([utils], [AS_HELP_STRING([--disable-utils],
            [don't build the WCS utilities])], [])
if test "x$enable_utils" = xno ; then
  AC_MSG_WARN([Compilation of WCS utilities disabled.])
else
  SUBDIRS="$SUBDIRS utils"
  INSTDIR="$INSTDIR utils"
fi

AC_SUBST([SUBDIRS])
AC_SUBST([TSTDIRS])
AC_SUBST([INSTDIR])


# Default observer coordinates for sundazel.
if test -f "$HOME/.sundazelrc"; then
  . "$HOME/.sundazelrc"
fi

if test "x$OBSLNG" = x; then
  OBSLNG=0.0
  OBSLAT=0.0
  OBSTZ=0.0
fi

AC_SUBST([OBSLNG])
AC_SUBST([OBSLAT])
AC_SUBST([OBSTZ])


# Tidy up incrementally defined variables.
FLFLAGS=`echo $FLFLAGS`
CPPFLAGS=`echo $CPPFLAGS`
CFLAGS=`echo $CFLAGS`
FFLAGS=`echo $FFLAGS`
LDFLAGS=`echo $LDFLAGS`

AC_MSG_NOTICE([End of auxiliary configuration.
])

# Set from the environment for code development.
AC_SUBST([FLAVOUR])
AC_SUBST([MODE])
AC_SUBST([VALGRIND])
AC_SUBST([EXTRA_CLEAN])


# Do it.
AC_MSG_NOTICE([Configuring files...])
AC_CONFIG_FILES([makedefs wcslib.pc])
AC_CONFIG_HEADERS([wcsconfig.h wcsconfig_f77.h wcsconfig_tests.h wcsconfig_utils.h])
AC_OUTPUT
