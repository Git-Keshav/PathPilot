import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || 'https://xyzcompany.supabase.co';
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || 'mock-anon-key';

// Dev mode: true when no real Supabase project is configured or using placeholder credentials
export const isDevMode = 
  !supabaseUrl ||
  supabaseUrl.includes('your-project') ||
  supabaseUrl.includes('xyzcompany') ||
  supabaseUrl.includes('pathpilot.supabase.co') ||
  supabaseUrl.includes('dummy') ||
  supabaseUrl.includes('mock') ||
  !supabaseAnonKey ||
  supabaseAnonKey === 'mock-anon-key' ||
  supabaseAnonKey.includes('your-supabase') ||
  supabaseAnonKey.includes('dummy');

export const supabase = createClient(
  isDevMode ? 'https://xyzcompany.supabase.co' : supabaseUrl,
  isDevMode ? 'mock-anon-key' : supabaseAnonKey,
  {
    auth: {
      persistSession: !isDevMode,
      autoRefreshToken: !isDevMode,
    },
  }
);
